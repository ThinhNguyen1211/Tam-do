// Tiny escaping template helper. Every interpolated value is HTML-escaped unless it is
// itself the output of `html` or `raw`, so API text can never inject markup.

class SafeHtml {
  constructor(value) {
    this.value = value;
  }
  toString() {
    return this.value;
  }
}

const ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
export const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ESCAPES[c]);

function fmt(v) {
  if (v == null || v === false) return '';
  if (Array.isArray(v)) return v.map(fmt).join('');
  if (v instanceof SafeHtml) return v.value;
  return esc(v);
}

export function html(strings, ...values) {
  let out = strings[0];
  for (let i = 0; i < values.length; i++) out += fmt(values[i]) + strings[i + 1];
  return new SafeHtml(out);
}

/** Mark trusted, developer-authored markup (e.g. bundled SVG) as safe. */
export const raw = (s) => new SafeHtml(String(s));

/**
 * The only innerHTML sink in the app; it accepts escaped templates and nothing else.
 * The CSP blocks style="" attributes, so templates mark sized elements with data-pct
 * and the value is applied here through CSSOM as --pct (CSS: calc(var(--pct) * 1%)).
 */
export function render(el, tpl) {
  if (!(tpl instanceof SafeHtml)) throw new TypeError('render() requires an html`` template');
  el.innerHTML = tpl.value;
  for (const node of el.querySelectorAll('[data-pct]')) {
    const pct = Number(node.dataset.pct);
    if (Number.isFinite(pct)) node.style.setProperty('--pct', String(Math.min(100, Math.max(0, pct))));
  }
}

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
