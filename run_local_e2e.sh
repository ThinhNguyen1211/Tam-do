#!/usr/bin/env bash
# Runs the whole stack locally — FastAPI on :8080 and the Vite frontend proxying /api to it —
# then verifies the browser-facing flow end to end through the frontend port, exactly as
# CloudFront would serve it (same origin, SHA-256 body header on POST).
#
# Usage: ./run_local_e2e.sh [--prod] [--check]
#   (default)  dev mode: Vite dev server on http://127.0.0.1:5173 with hot reload
#   --prod     production bundle: `vite build` + `vite preview` on http://127.0.0.1:4173,
#              sending the same CSP and security headers as CloudFront
#   --check    verify, stop both servers and exit with the result (for scripts/CI)
#
# Without --check the servers keep running and both logs stream here; Ctrl+C stops everything.
# Needs: python (3.11+), node/npm, curl. Creates backend/.venv on first run.
set -euo pipefail

MODE=dev
CHECK_ONLY=false
for arg in "$@"; do
  case "$arg" in
    --prod) MODE=prod ;;
    --check) CHECK_ONLY=true ;;
    -h | --help) sed -n '2,13p' "$0"; exit 0 ;;
    *) printf 'Unknown option: %s (try --help)\n' "$arg" >&2; exit 2 ;;
  esac
done

# Same port as the Lambda container (AWS_LWA_PORT). Hyper-V/WSL2 sometimes reserves it on
# Windows; port_excluded below reports that clearly instead of failing to connect.
API_PORT=8080
# Loopback only by default. Set API_BIND_HOST=0.0.0.0 to reach it from WSL2/containers
# (that also exposes it to the LAN). Clients always use 127.0.0.1, never "localhost",
# which may resolve to ::1 (IPv6) where nothing is listening.
API_BIND_HOST="${API_BIND_HOST:-127.0.0.1}"
API_URL="http://127.0.0.1:$API_PORT"
if [[ $MODE == prod ]]; then WEB_PORT=4173; else WEB_PORT=5173; fi
WEB_URL="http://127.0.0.1:$WEB_PORT"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NATIVE_ROOT="$ROOT_DIR" # path form that native Windows programs (python, node) understand
IS_WINDOWS=false
case "$(uname -s)" in
  MINGW* | MSYS* | CYGWIN*) NATIVE_ROOT="$(cygpath -m "$ROOT_DIR")"; IS_WINDOWS=true ;;
esac
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
LOG_DIR="$ROOT_DIR/.local-e2e"
VENV_DIR="$BACKEND_DIR/.venv"

log() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
die() { printf '\033[1;31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

for cmd in node npm curl; do
  command -v "$cmd" >/dev/null 2>&1 || die "'$cmd' is not installed or not on PATH"
done

# --- process handling ------------------------------------------------------------
backend_pid=""
frontend_pid=""

stop_process() {
  local pid="$1"
  [[ -n $pid ]] || return 0
  # In Git Bash, $! is an MSYS pid; kill the Windows process tree behind it as well.
  if [[ -r /proc/$pid/winpid ]] && command -v taskkill.exe >/dev/null 2>&1; then
    taskkill.exe //F //T //PID "$(cat "/proc/$pid/winpid")" >/dev/null 2>&1 || true
  fi
  kill "$pid" 2>/dev/null || true
}

cleanup() {
  trap - EXIT INT TERM
  stop_process "$frontend_pid"
  stop_process "$backend_pid"
  echo "Stopped local servers. Logs: $LOG_DIR"
}
trap cleanup EXIT
trap 'exit 130' INT TERM

listeners_on() { # prints the processes listening on TCP port $1 (any address), if any
  if $IS_WINDOWS; then
    local pid
    for pid in $(netstat -ano -p TCP 2>/dev/null | tr -d '\r' | awk -v p=":$1" '$4 == "LISTENING" && substr($2, length($2) - length(p) + 1) == p { print $5 }' | sort -u); do
      printf '    %s\n' "$(tasklist.exe //FI "PID eq $pid" //FO CSV //NH 2>/dev/null | tr -d '\r' | cut -d, -f1,2 | tr -d '"' | sed 's/,/  pid /')"
    done
    netstat -ano -p TCPv6 2>/dev/null | tr -d '\r' | awk -v p=":$1" '$4 == "LISTENING" && substr($2, length($2) - length(p) + 1) == p { print "    IPv6 listener " $2 "  pid " $5 }' | sort -u
  elif command -v ss >/dev/null 2>&1; then
    ss -Hltnp "sport = :$1" 2>/dev/null | sed 's/^/    /'
  elif command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"$1" -sTCP:LISTEN 2>/dev/null | sed 's/^/    /'
  fi
}

port_excluded() { # Windows only: is TCP port $1 inside a reserved (Hyper-V/WSL/admin) range?
  $IS_WINDOWS || return 1
  netsh.exe interface ipv4 show excludedportrange protocol=tcp 2>/dev/null | tr -d '\r' \
    | awk -v p="$1" '$1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ && p >= $1 && p <= $2 { print "    reserved range " $1 "-" $2; found = 1 } END { exit !found }'
}

port_in_use() { # open on 127.0.0.1, or any listener at all (e.g. [::1] only)
  (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null || [[ -n "$(listeners_on "$1")" ]]
}

# curl without proxies: an HTTP(S)_PROXY or .curlrc would otherwise send local checks away.
probe() { curl -sS --noproxy '*' --max-time 3 -o /dev/null -w '%{http_code}' "$@"; }

wait_for() { # wait_for <url> <name> <pid> <port>
  local url="$1" name="$2" pid="$3" port="$4" code msg last="" second
  echo "  waiting for $name at $url (up to 60s)"
  for second in $(seq 1 60); do
    if code="$(probe "$url" 2>"$LOG_DIR/curl.err")" && [[ $code == 2* ]]; then
      echo "  $name ready after ${second}s (HTTP $code)"
      return 0
    fi
    # Drop curl's per-attempt timing ("after 2036 ms") so a repeating error is recognised.
    msg="$(tr -d '\r' <"$LOG_DIR/curl.err" | sed -E 's/ after [0-9]+ ms//')"
    msg="${msg:-HTTP ${code:-000}}"
    # Print each new error, and a heartbeat every 10s while it stays the same.
    if [[ $msg != "$last" || $((second % 10)) -eq 0 ]]; then printf '  [%2ds] %s\n' "$second" "$msg"; fi
    last="$msg"
    if ! kill -0 "$pid" 2>/dev/null; then
      printf '\n  %s exited during startup. Last lines of %s:\n' "$name" "$LOG_DIR/$name.log"
      tail -n 20 "$LOG_DIR/$name.log" | sed 's/^/    /'
      die "$name exited during startup"
    fi
    sleep 1
  done
  printf '\n  Diagnosis for %s:\n    last curl error: %s\n    listeners on port %s:\n' "$name" "$last" "$port"
  listeners_on "$port" || true
  printf '    verbose curl:\n'
  { curl -sv --noproxy '*' --max-time 3 -o /dev/null "$url" 2>&1 || true; } | sed 's/^/      /' | head -n 15 || true
  printf '    last lines of %s:\n' "$LOG_DIR/$name.log"
  tail -n 20 "$LOG_DIR/$name.log" | sed 's/^/      /'
  die "$name did not answer at $url within 60s"
}

mkdir -p "$LOG_DIR"
for port in "$API_PORT" "$WEB_PORT"; do
  if port_excluded "$port" >&2; then
    die "Port $port is reserved by Windows (netsh interface ipv4 show excludedportrange protocol=tcp); pick another port or restart the winnat service"
  fi
  if port_in_use "$port"; then
    printf '\033[1;31mPort %s is already in use by:\033[0m\n' "$port" >&2
    listeners_on "$port" >&2 || true
    die "Stop whatever is listening on port $port first"
  fi
done

# --- backend environment ---------------------------------------------------------
if [[ -x $VENV_DIR/Scripts/python.exe ]]; then
  VENV_PY="$VENV_DIR/Scripts/python.exe"
else
  VENV_PY="$VENV_DIR/bin/python"
fi

if [[ ! -x $VENV_PY ]]; then
  log "Creating backend virtualenv ($VENV_DIR)"
  host_py=""
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then
      host_py="$candidate"
      break
    fi
  done
  [[ -n $host_py ]] || die "Python 3.11+ not found (tried python3, python)"
  "$host_py" -m venv "$VENV_DIR"
  [[ -x $VENV_DIR/Scripts/python.exe ]] && VENV_PY="$VENV_DIR/Scripts/python.exe"
fi

# Reinstall only when the requirement files change.
req_stamp="$(cat "$BACKEND_DIR/requirements.txt" "$BACKEND_DIR/requirements-dev.txt" | cksum)"
if [[ "$(cat "$VENV_DIR/.requirements-stamp" 2>/dev/null)" != "$req_stamp" ]]; then
  log "Installing backend dependencies"
  "$VENV_PY" -m pip install --quiet --disable-pip-version-check \
    -r "$BACKEND_DIR/requirements.txt" -r "$BACKEND_DIR/requirements-dev.txt"
  printf '%s' "$req_stamp" >"$VENV_DIR/.requirements-stamp"
fi

if [[ ! -d $FRONTEND_DIR/node_modules ]]; then
  log "Installing frontend dependencies"
  npm --prefix "$FRONTEND_DIR" ci --no-audit --no-fund
fi
VITE=(node "$NATIVE_ROOT/frontend/node_modules/vite/bin/vite.js")

# --- start servers ---------------------------------------------------------------
echo "  python: $("$VENV_PY" --version 2>&1)   node: $(node --version)   curl: $(curl --version | head -n 1 | cut -d' ' -f1-2)"

log "Starting FastAPI on $API_BIND_HOST:$API_PORT"
(cd "$BACKEND_DIR" && exec "$VENV_PY" -m uvicorn app.main:app --host "$API_BIND_HOST" --port "$API_PORT") \
  >"$LOG_DIR/backend.log" 2>&1 &
backend_pid=$!
wait_for "$API_URL/api/health" backend "$backend_pid" "$API_PORT"

# Pin Vite to 127.0.0.1: its default "localhost" can bind IPv6-only on Windows.
export VITE_PROXY_TARGET="$API_URL" # vite.config.js proxies /api here
if [[ $MODE == prod ]]; then
  log "Building production bundle"
  (cd "$FRONTEND_DIR" && "${VITE[@]}" build) >"$LOG_DIR/build.log" 2>&1 \
    || die "Frontend build failed; see $LOG_DIR/build.log"
  log "Starting vite preview on $WEB_URL (with CloudFront security headers)"
  (cd "$FRONTEND_DIR" && exec "${VITE[@]}" preview --host 127.0.0.1) >"$LOG_DIR/frontend.log" 2>&1 &
else
  log "Starting Vite dev server on $WEB_URL"
  (cd "$FRONTEND_DIR" && exec "${VITE[@]}" --host 127.0.0.1) >"$LOG_DIR/frontend.log" 2>&1 &
fi
frontend_pid=$!
wait_for "$WEB_URL/" frontend "$frontend_pid" "$WEB_PORT"

# --- verify through the frontend origin ------------------------------------------
log "Verifying $WEB_URL"
# The checks run in the backend venv's Python: stdlib only, and it can hash the exact
# request body the same way the browser does for x-amz-content-sha256.
verify_status=0
"$VENV_PY" - "$WEB_URL" "$MODE" "$NATIVE_ROOT/frontend/csp.json" <<'PY' || verify_status=$?
import hashlib, json, random, re, sys, urllib.request

base, mode, csp_path = sys.argv[1:4]
sys.stdout.reconfigure(encoding="utf-8")  # Windows pipes default to cp1252; titles are Vietnamese
failures = 0

def check(name, ok, detail=""):
    global failures
    failures += not ok
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))

# No proxies: urllib otherwise honours HTTP_PROXY and, on Windows, the system proxy settings.
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def fetch(path, body=None, headers=None):
    req = urllib.request.Request(base + path, data=body, headers=headers or {})
    with opener.open(req, timeout=20) as resp:
        return resp.status, resp.headers, resp.read().decode("utf-8")

status, headers, page = fetch("/")
check("GET / serves the app shell", status == 200 and "Tâm Đồ" in page)

if mode == "prod":
    with open(csp_path, encoding="utf-8") as f:
        expected_csp = "; ".join(json.load(f)["directives"])
    check("CSP header matches frontend/csp.json", headers.get("Content-Security-Policy") == expected_csp)
    check("X-Frame-Options: DENY", headers.get("X-Frame-Options") == "DENY")
    check("X-Content-Type-Options: nosniff", headers.get("X-Content-Type-Options") == "nosniff")
    assets = re.findall(r'(?:src|href)="(/[^"]+\.(?:js|css))"', page)
    check("Bundle assets load", bool(assets) and all(fetch(a)[0] == 200 for a in assets), f"{len(assets)} files")

status, _, body = fetch("/api/health")
check("GET /api/health via frontend proxy", status == 200 and json.loads(body).get("status") == "ok")

status, _, body = fetch("/api/questions?count=25")
questions = json.loads(body)
check("GET /api/questions?count=25", status == 200 and len(questions) == 25, f"{len(questions)} questions")

answers = [{"question_id": q["id"], "score": random.randint(-3, 3)} for q in questions]
payload = json.dumps({"answers": answers}).encode("utf-8")
status, _, body = fetch("/api/submit", payload, {
    "Content-Type": "application/json",
    "x-amz-content-sha256": hashlib.sha256(payload).hexdigest(),
})
result = json.loads(body)
check("POST /api/submit with SHA-256 header", status == 200 and re.fullmatch(r"[EI][SN][TF][JP]", result.get("mbti_type", "")) is not None,
      f"{result.get('mbti_type')} — {result.get('type_title')}")
check("Result has all 4 profile sections", len(result.get("psychological_profile", {})) == 4)

sys.exit(1 if failures else 0)
PY

if $CHECK_ONLY; then
  [[ $verify_status -eq 0 ]] || die "Local checks failed"
  log "All local checks passed"
  exit 0
fi
# Interactive mode keeps the servers up even if a check failed, so it can be debugged.
[[ $verify_status -eq 0 ]] || printf '\033[1;33mSome checks failed; servers left running for debugging.\033[0m\n'

cat <<EOF

  App:       $WEB_URL
  API:       $API_URL/api/health   (bound to $API_BIND_HOST)
  API docs:  $API_URL/api/docs
  Logs:      $LOG_DIR/{backend,frontend}.log

Streaming logs — press Ctrl+C to stop both servers.
EOF
tail -n 0 -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log"
