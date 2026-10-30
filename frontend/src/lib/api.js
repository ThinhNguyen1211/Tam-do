// Production: same-origin `/api` behind CloudFront. Local dev: Vite proxies `/api`,
// or set VITE_API_BASE (e.g. http://127.0.0.1:8080/api) to call a backend directly.
const API_BASE = (import.meta.env.VITE_API_BASE || '/api').replace(/\/+$/, '');
const TIMEOUT_MS = 20000;

export class ApiError extends Error {
  constructor(status, detail) {
    super(typeof detail === 'string' ? detail : `HTTP ${status}`);
    this.status = status;
  }
}

async function request(path, init = {}) {
  let res;
  try {
    res = await fetch(API_BASE + path, {
      ...init,
      headers: { Accept: 'application/json', ...init.headers },
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
  } catch (err) {
    throw new ApiError(0, err?.name === 'TimeoutError' ? 'timeout' : 'network');
  }
  if (!res.ok) {
    let detail;
    try {
      detail = (await res.json()).detail;
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, detail);
  }
  return res.json();
}

export async function sha256Hex(text) {
  const digest = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export const fetchQuestions = (count) => request(`/questions?count=${encodeURIComponent(count)}`);

export async function submitAnswers(answers) {
  // CloudFront OAC signs requests to the Lambda Function URL with SigV4, which needs the
  // payload hash from the client. It must be the hash of the exact bytes sent.
  const body = JSON.stringify({ answers });
  return request('/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-amz-content-sha256': await sha256Hex(body) },
    body,
  });
}
