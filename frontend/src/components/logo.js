import logoSvg from '../assets/logo.svg?raw';
import { html, raw } from '../lib/dom.js';

// Inlined (not <img>) so CSS can recolour the strokes per theme and animate the petals.
export const logo = (className = '') => html`<span class="logo ${className}" aria-hidden="true">${raw(logoSvg)}</span>`;

export const wordmark = () => html`
  <span class="wordmark">
    ${logo('logo--sm')}
    <span class="wordmark__text">Tâm Đồ</span>
  </span>
`;
