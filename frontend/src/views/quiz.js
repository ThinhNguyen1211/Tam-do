import { fetchQuestions } from '../lib/api.js';
import { LIKERT } from '../lib/content.js';
import { $, html, render } from '../lib/dom.js';
import { KEYS, tabState } from '../lib/storage.js';

const ADVANCE_DELAY_MS = 260; // long enough to see the selection land

export function quizView(root, params, go) {
  let state = null; // { questions, answers: {id: score}, index }
  let dir = 'forward';
  let advanceTimer = null;
  let disposed = false;

  const save = () => tabState.set(KEYS.progress, state);
  const answeredCount = () => Object.keys(state.answers).length;
  const complete = () => answeredCount() === state.questions.length;

  function paintLoading() {
    render(
      root,
      html`<section class="container quiz" aria-busy="true">
        <div class="card card--glass question-card question-card--skeleton">
          <h1 class="visually-hidden" tabindex="-1" data-autofocus>Đang tải câu hỏi</h1>
          <div class="skeleton skeleton--line"></div>
          <div class="skeleton skeleton--line skeleton--short"></div>
        </div>
      </section>`,
    );
  }

  function paintError() {
    render(
      root,
      html`<section class="container quiz">
        <div class="card card--glass notice" role="alert">
          <h1 tabindex="-1" data-autofocus>Không tải được câu hỏi</h1>
          <p>Vui lòng kiểm tra kết nối mạng và thử lại.</p>
          <div class="notice__actions">
            <button type="button" class="btn btn--primary" data-retry>Thử lại</button>
            <button type="button" class="btn btn--ghost" data-exit>Về trang chủ</button>
          </div>
        </div>
      </section>`,
    );
  }

  function paint() {
    const q = state.questions[state.index];
    const total = state.questions.length;
    const answered = answeredCount();
    const pct = Math.round((answered / total) * 100);
    const current = state.answers[q.id];
    const isLast = state.index === total - 1;

    render(
      root,
      html`
        <section class="container quiz">
          <div class="progress" aria-label="Tiến độ">
            <div class="progress__meta">
              <span>Câu <strong>${state.index + 1}</strong> / ${total}</span>
              <span>${pct}% hoàn thành</span>
            </div>
            <div class="progress__track" role="progressbar" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${answered}" aria-valuetext="Đã trả lời ${answered} trên ${total} câu">
              <div class="progress__fill" data-pct="${pct}"></div>
            </div>
          </div>

          <article class="card card--glass question-card" data-dir="${dir}">
            <p class="question-card__index">Câu ${state.index + 1}</p>
            <h1 class="question-card__text" id="q-text" tabindex="-1" data-autofocus>${q.text}</h1>
            <p class="question-card__en" lang="en">${q.text_en}</p>

            <div class="likert" role="radiogroup" aria-labelledby="q-text">
              ${LIKERT.map(
                (opt, i) => html`
                  <button type="button" class="likert__opt" role="radio" data-score="${opt.score}" data-weight="${Math.abs(opt.score)}"
                    data-side="${opt.score > 0 ? 'agree' : opt.score < 0 ? 'disagree' : 'neutral'}"
                    aria-checked="${current === opt.score}" aria-label="${opt.label}" tabindex="${(current ?? 0) === opt.score ? 0 : -1}">
                    <span class="likert__dot"></span>
                    <span class="likert__label">${opt.label}</span>
                    <kbd class="likert__key">${i + 1}</kbd>
                  </button>
                `,
              )}
            </div>
          </article>

          <nav class="quiz-nav" aria-label="Điều hướng câu hỏi">
            <button type="button" class="btn btn--ghost" data-prev ${state.index === 0 ? html`disabled` : ''}>
              ← Trở về câu trước
            </button>
            ${complete()
              ? html`<button type="button" class="btn btn--primary" data-submit>Xem kết quả →</button>`
              : !isLast && current !== undefined
                ? html`<button type="button" class="btn btn--ghost" data-next>Câu tiếp →</button>`
                : ''}
          </nav>
          <p class="quiz-hint">Phím tắt: <kbd>1</kbd>–<kbd>7</kbd> để chọn · <kbd>←</kbd> câu trước · <kbd>→</kbd> câu tiếp</p>
          <button type="button" class="link-btn quiz-exit" data-exit>Tạm dừng và về trang chủ</button>
        </section>
      `,
    );
  }

  function moveTo(index, direction) {
    if (index < 0 || index >= state.questions.length) return;
    dir = direction;
    state.index = index;
    save();
    paint();
    $('[data-autofocus]', root)?.focus({ preventScroll: true });
  }

  function choose(score) {
    const q = state.questions[state.index];
    state.answers[q.id] = score;
    save();
    clearTimeout(advanceTimer);
    // Re-render for the selected state, then glide to the next unanswered-or-next question.
    paint();
    $(`.likert__opt[data-score="${score}"]`, root)?.focus({ preventScroll: true });
    if (state.index < state.questions.length - 1) {
      advanceTimer = setTimeout(() => moveTo(state.index + 1, 'forward'), ADVANCE_DELAY_MS);
    } else if (complete()) {
      $('[data-submit]', root)?.focus();
    }
  }

  function submit() {
    if (!complete()) return;
    const answers = state.questions.map((q) => ({ question_id: q.id, score: state.answers[q.id] }));
    go('loading', { answers });
  }

  const onClick = (e) => {
    const opt = e.target.closest('.likert__opt');
    if (opt) return choose(Number(opt.dataset.score));
    if (e.target.closest('[data-prev]')) return moveTo(state.index - 1, 'back');
    if (e.target.closest('[data-next]')) return moveTo(state.index + 1, 'forward');
    if (e.target.closest('[data-submit]')) return submit();
    if (e.target.closest('[data-retry]')) return start();
    if (e.target.closest('[data-exit]')) return go('landing');
  };

  const onKey = (e) => {
    if (!state || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key >= '1' && e.key <= '7') {
      e.preventDefault();
      return choose(LIKERT[Number(e.key) - 1].score);
    }
    if (e.key === 'ArrowLeft' || (e.key === 'Backspace' && e.target === document.body)) {
      e.preventDefault();
      return moveTo(state.index - 1, 'back');
    }
    if (e.key === 'ArrowRight' && state.answers[state.questions[state.index].id] !== undefined) {
      e.preventDefault();
      return moveTo(state.index + 1, 'forward');
    }
    if (e.key === 'Enter' && complete() && !e.target.closest('button')) {
      e.preventDefault();
      submit();
    }
  };

  async function start() {
    const saved = params.resume ? tabState.get(KEYS.progress) : null;
    if (saved?.questions?.length) {
      state = saved;
      return paint();
    }
    paintLoading();
    try {
      const questions = await fetchQuestions(params.count ?? 50);
      if (disposed) return;
      state = { questions, answers: {}, index: 0 };
      save();
      paint();
      $('[data-autofocus]', root)?.focus({ preventScroll: true });
    } catch {
      if (!disposed) paintError();
    }
  }

  root.addEventListener('click', onClick);
  document.addEventListener('keydown', onKey);
  start();

  return () => {
    disposed = true;
    clearTimeout(advanceTimer);
    root.removeEventListener('click', onClick);
    document.removeEventListener('keydown', onKey);
  };
}
