#!/usr/bin/env bash
# Single-command deploy of the full stack:
#   1. clean production build of the frontend (fails fast, before anything in AWS changes)
#   2. backend image build + push to ECR
#   3. terraform apply
#   4. frontend sync to S3 + CloudFront invalidation
#   5. smoke tests of / and /api/* (including security headers) on the CloudFront domain
#
# The Lambda function cannot be created until its image exists in ECR, so the
# repository is applied on its own first, then the image is pushed, then the rest.
#
# Docker: uses a native `docker` if its daemon answers, otherwise Docker inside WSL
# (`wsl.exe -e docker`), which is the setup on Windows hosts without Docker Desktop.
#
# Usage: ./build_and_deploy_infra.sh [image-tag]   (default: UTC timestamp)
set -euo pipefail

AWS_PROFILE="${AWS_PROFILE:-tamdo}"
AWS_REGION="${AWS_REGION:-ap-southeast-1}"
IMAGE_TAG="${1:-$(date -u +%Y%m%d%H%M%S)}"
PLATFORM="${PLATFORM:-linux/amd64}"   # must match var.lambda_architecture (x86_64)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "$(uname -s)" in
  MINGW* | MSYS* | CYGWIN*)
    # Git Bash rewrites /-prefixed arguments for Windows programs, which mangles
    # values like the invalidation path '/*'. Use C:/... paths and turn that off.
    ROOT_DIR="$(cygpath -m "$ROOT_DIR")"
    export MSYS_NO_PATHCONV=1
    ;;
esac
TF_DIR="$ROOT_DIR/terraform"
FRONTEND_DIR="$ROOT_DIR/frontend"
DIST="$FRONTEND_DIR/dist"
export AWS_PROFILE AWS_REGION

log() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
die() { printf '\033[1;31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

for cmd in aws terraform curl npm; do
  command -v "$cmd" >/dev/null 2>&1 || die "'$cmd' is not installed or not on PATH"
done

# --- pick a Docker engine -------------------------------------------------------
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  DOCKER=(docker)
  docker_path() { printf '%s' "$1"; }
elif command -v wsl.exe >/dev/null 2>&1 && wsl.exe -e docker info >/dev/null 2>&1; then
  DOCKER=(wsl.exe -e docker)
  # The build context must be given as a path inside WSL (/mnt/c/...).
  docker_path() { wsl.exe -e wslpath -a "$1" | tr -d '\r'; }
else
  die "No working Docker found (tried native docker and 'wsl.exe -e docker')"
fi
echo "Using Docker: ${DOCKER[*]}"

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)" \
  || die "AWS profile '$AWS_PROFILE' is not authenticated"
log "Deploying to AWS account $ACCOUNT_ID (profile $AWS_PROFILE, region $AWS_REGION)"

log "Building frontend (clean install + production bundle)"
rm -rf "$DIST"
npm --prefix "$FRONTEND_DIR" ci --no-audit --no-fund
npm --prefix "$FRONTEND_DIR" run build
[[ -f "$DIST/index.html" ]] || die "Frontend build produced no $DIST/index.html"

tf() { terraform -chdir="$TF_DIR" "$@"; }
TF_VARS=(-var "aws_profile=$AWS_PROFILE" -var "aws_region=$AWS_REGION" -var "image_tag=$IMAGE_TAG")

log "terraform init"
tf init -input=false

log "Creating ECR repository"
tf apply -input=false -auto-approve "${TF_VARS[@]}" \
  -target=aws_ecr_repository.backend -target=aws_ecr_lifecycle_policy.backend

ECR_URL="$(tf output -raw ecr_repository_url)"
REGISTRY="${ECR_URL%%/*}"

log "Logging in to ECR ($REGISTRY)"
aws ecr get-login-password | "${DOCKER[@]}" login --username AWS --password-stdin "$REGISTRY"

log "Building backend image $ECR_URL:$IMAGE_TAG ($PLATFORM)"
# --provenance=false: Lambda rejects the multi-manifest index that buildx attestations produce.
"${DOCKER[@]}" buildx build \
  --platform "$PLATFORM" \
  --provenance=false \
  --tag "$ECR_URL:$IMAGE_TAG" \
  --push \
  "$(docker_path "$ROOT_DIR/backend")"

log "Applying full infrastructure"
tf apply -input=false -auto-approve "${TF_VARS[@]}"

BUCKET="$(tf output -raw s3_bucket_name)"
DIST_ID="$(tf output -raw cloudfront_distribution_id)"
APP_URL="$(tf output -raw cloudfront_domain_name)"

log "Syncing frontend to s3://$BUCKET"
# Vite fingerprints everything under assets/, so it can be cached forever. Everything else
# (index.html, theme-init.js) keeps its name across deploys and must always be revalidated.
aws s3 sync "$DIST/assets" "s3://$BUCKET/assets" --delete \
  --cache-control "public, max-age=31536000, immutable"
aws s3 sync "$DIST" "s3://$BUCKET" --delete --exclude 'assets/*' \
  --cache-control "no-cache"

log "Invalidating CloudFront cache"
aws cloudfront create-invalidation --distribution-id "$DIST_ID" --paths '/*' >/dev/null

log "Smoke-testing $APP_URL (a new distribution can take several minutes to deploy)"
for attempt in $(seq 1 30); do
  if curl -fsS "$APP_URL/api/health" >/dev/null 2>&1; then
    echo "Health OK after $attempt attempt(s)"
    break
  fi
  [[ $attempt -eq 30 ]] && die "API did not become healthy at $APP_URL/api/health"
  sleep 20
done

failures=0
check() { # check <description> <command...>
  if "${@:2}"; then echo "  PASS  $1"; else echo "  FAIL  $1"; failures=$((failures + 1)); fi
}

# One request, headers and body split at the first blank line. Not `-o /dev/null`: with
# MSYS_NO_PATHCONV set, a Windows curl.exe receives that path unconverted and fails (exit 23).
home_response="$(curl -fsS -D - "$APP_URL/")"
home_headers="${home_response%%$'\r\n\r\n'*}"
home_body="${home_response#*$'\r\n\r\n'}"
health_body="$(curl -fsS "$APP_URL/api/health")"
questions_json="$(curl -fsS "$APP_URL/api/questions?count=25")"
has_header() { grep -qi "^$1:" <<<"$home_headers"; }

check "GET / serves the Tâm Đồ app"       grep -q 'Tâm Đồ' <<<"$home_body"
check "GET /api/health reports ok"        grep -q '"ok"' <<<"$health_body"
check "GET /api/questions?count=25"       grep -q '"dichotomy"' <<<"$questions_json"
check "Strict-Transport-Security header"  has_header strict-transport-security
check "Content-Security-Policy header"    has_header content-security-policy
check "X-Frame-Options header"            has_header x-frame-options
check "X-Content-Type-Options header"     has_header x-content-type-options
check "Referrer-Policy header"            has_header referrer-policy
[[ $failures -eq 0 ]] || die "$failures smoke test(s) failed"

log "Done"
echo "App: $APP_URL"
