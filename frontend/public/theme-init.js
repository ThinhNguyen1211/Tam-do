// Applies the saved theme before first paint to avoid a flash of the wrong theme.
// A separate classic script (not inline) so the CSP can stay `script-src 'self'`.
try {
  // Stored JSON-encoded by src/lib/storage.js.
  var t = JSON.parse(localStorage.getItem('tamdo-theme'));
  if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
} catch (e) {}
