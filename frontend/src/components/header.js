import { html, render } from '../lib/dom.js';
import { getTheme, toggleTheme } from '../lib/theme.js';
import { wordmark } from './logo.js';

const SUN = html`<svg viewBox="0 0 24 24" class="icon" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>`;
const MOON = html`<svg viewBox="0 0 24 24" class="icon" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z"/></svg>`;

export function mountHeader(el, { onHome }) {
  const paint = () => {
    const dark = getTheme() === 'dark';
    render(
      el,
      html`
        <div class="container site-header__inner">
          <a href="./" class="site-header__home" data-home aria-label="Tâm Đồ — Trang chủ">${wordmark()}</a>
          <button type="button" class="icon-btn" data-theme-toggle aria-label="${dark ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối'}">
            ${dark ? SUN : MOON}
          </button>
        </div>
      `,
    );
  };
  el.addEventListener('click', (e) => {
    if (e.target.closest('[data-theme-toggle]')) {
      toggleTheme();
      paint();
      el.querySelector('[data-theme-toggle]').focus();
    } else if (e.target.closest('[data-home]')) {
      e.preventDefault();
      onHome();
    }
  });
  paint();
}
