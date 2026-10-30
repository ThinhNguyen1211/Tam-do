import { submitAnswers } from '../lib/api.js';
import { html, render } from '../lib/dom.js';
import { KEYS, prefs, tabState } from '../lib/storage.js';

// Scoring takes milliseconds; a short floor keeps the transition calm instead of a flash.
const MIN_DISPLAY_MS = 1600;
const MESSAGES = [
  'Đang lắng nghe các câu trả lời của bạn…',
  'Đang cân bằng bốn chiều tính cách…',
  'Đang sắp xếp các chức năng nhận thức…',
];

export function loadingView(root, { answers }, go) {
  let disposed = false;
  let msgIndex = 0;

  render(
    root,
    html`
      <section class="container loading" aria-live="polite">
        <div class="pulse" aria-hidden="true">
          <span class="pulse__ring"></span>
          <span class="pulse__ring"></span>
          <span class="pulse__ring"></span>
          <span class="pulse__core"></span>
        </div>
        <h1 class="loading__title" tabindex="-1" data-autofocus>Đang phân tích hồ sơ tâm lý</h1>
        <p class="loading__msg" data-msg>${MESSAGES[0]}</p>
      </section>
    `,
  );

  const msgEl = root.querySelector('[data-msg]');
  const ticker = setInterval(() => {
    msgIndex = (msgIndex + 1) % MESSAGES.length;
    msgEl.textContent = MESSAGES[msgIndex];
  }, 1400);

  const minDelay = new Promise((r) => setTimeout(r, MIN_DISPLAY_MS));
  Promise.all([submitAnswers(answers), minDelay])
    .then(([result]) => {
      if (disposed) return;
      prefs.set(KEYS.lastResult, result);
      tabState.set(KEYS.progress, null);
      go('result', { result });
    })
    .catch(() => {
      if (disposed) return;
      clearInterval(ticker);
      render(
        root,
        html`
          <section class="container loading">
            <div class="card card--glass notice" role="alert">
              <h1 tabindex="-1" data-autofocus>Chưa gửi được câu trả lời</h1>
              <p>Câu trả lời của bạn vẫn được giữ nguyên. Vui lòng thử lại sau giây lát.</p>
              <div class="notice__actions">
                <button type="button" class="btn btn--primary" data-retry>Thử lại</button>
                <button type="button" class="btn btn--ghost" data-back>Quay lại bài làm</button>
              </div>
            </div>
          </section>
        `,
      );
      root.querySelector('[data-autofocus]')?.focus();
      root.querySelector('[data-retry]').addEventListener('click', () => go('loading', { answers }));
      root.querySelector('[data-back]').addEventListener('click', () => go('quiz', { resume: true }));
    });

  return () => {
    disposed = true;
    clearInterval(ticker);
  };
}
