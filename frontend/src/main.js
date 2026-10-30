import '@fontsource/be-vietnam-pro/400.css';
import '@fontsource/be-vietnam-pro/500.css';
import '@fontsource/be-vietnam-pro/600.css';
import '@fontsource-variable/lora';
import './styles/tokens.css';
import './styles/base.css';
import './styles/components.css';
import './styles/views.css';

import { mountHeader } from './components/header.js';
import { FOOTER_NOTE } from './lib/content.js';
import { html, render } from './lib/dom.js';
import { landingView } from './views/landing.js';
import { loadingView } from './views/loading.js';
import { quizView } from './views/quiz.js';
import { resultView } from './views/result.js';

// A view is `(root, params, go) => cleanup?`. The app is a small state machine:
// landing -> quiz -> loading -> result, with "back to landing" from anywhere.
const VIEWS = { landing: landingView, quiz: quizView, loading: loadingView, result: resultView };

const root = document.getElementById('main');
let cleanup = null;

function go(name, params = {}) {
  cleanup?.();
  cleanup = null;
  root.dataset.view = name;
  cleanup = VIEWS[name](root, params, go) ?? null;
  // On <html> because the document is the scroller; CSS enables scroll snap for the landing view
  // only. Set after rendering: enabling snap while <main> is empty makes the footer the snapped
  // element, and the browser then re-snaps to it (the page bottom) once the content appears.
  document.documentElement.dataset.view = name;
  window.scrollTo({ top: 0, behavior: 'instant' });
  // Move focus to the new view's heading so screen readers announce the change.
  root.querySelector('[data-autofocus]')?.focus({ preventScroll: true });
}

mountHeader(document.getElementById('site-header'), { onHome: () => go('landing') });
render(document.getElementById('site-footer'), html`<p>${FOOTER_NOTE}</p>`);
go('landing');
