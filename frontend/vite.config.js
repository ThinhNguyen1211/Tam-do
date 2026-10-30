import { readFileSync } from 'node:fs';
import { defineConfig } from 'vite';

// Same policy CloudFront sends (terraform/cloudfront.tf reads this file too).
const csp = JSON.parse(readFileSync(new URL('./csp.json', import.meta.url), 'utf8')).directives.join('; ');

// Mirrors the CloudFront response headers policy, minus HSTS (meaningless over http://).
// Only `vite preview` gets these: the dev server injects <style> tags for HMR, which the CSP blocks.
const securityHeaders = {
  'Content-Security-Policy': csp,
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
};

// /api is proxied to the local FastAPI server so the app stays same-origin,
// exactly like production where CloudFront serves both.
const apiProxy = {
  '/api': { target: process.env.VITE_PROXY_TARGET ?? 'http://127.0.0.1:8080', changeOrigin: true },
};

export default defineConfig({
  server: {
    port: 5173,
    strictPort: true,
    proxy: apiProxy,
  },
  preview: {
    port: 4173,
    strictPort: true,
    proxy: apiProxy,
    headers: securityHeaders,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: 'es2020',
    // Never inline assets as data: URIs; the CSP (img-src 'self', font-src 'self') blocks them.
    assetsInlineLimit: 0,
  },
});
