import { logo } from '../components/logo.js';
import { DICHOTOMIES, FOOTER_NOTE, FUNCTIONS, LANDING, LENGTHS, POLES, POLES_EN } from '../lib/content.js';
import { $$, html, render } from '../lib/dom.js';
import { createFullPage } from '../lib/fullpage.js';
import { KEYS, prefs, tabState } from '../lib/storage.js';

// Three full-screen sections. Each `.snap-section` is exactly one viewport tall (below the
// header); its `__inner` wrapper centres the content when it fits and scrolls when it doesn't.
export function landingView(root, _params, go) {
  let selected = LENGTHS.find((l) => l.recommended).count;
  const lastResult = prefs.get(KEYS.lastResult);
  const progress = tabState.get(KEYS.progress);
  const answered = progress ? Object.keys(progress.answers).length : 0;

  render(
    root,
    html`
      <section class="snap-section" aria-label="${LANDING.sections[0]}">
        <div class="snap-section__inner container hero">
          <div class="hero__copy">
            <h1 class="hero__title" tabindex="-1" data-autofocus>${LANDING.heroTitle}</h1>
            <p class="hero__lede">${LANDING.heroIntro}</p>
          </div>

          <div class="card card--glass start-card">
            <div class="start-card__logo">${logo('logo--hero')}</div>
            <h2 class="start-card__title" id="length-label">Chọn độ dài bài kiểm tra</h2>
            <div class="pills" role="radiogroup" aria-labelledby="length-label">
              ${LENGTHS.map(
                (l) => html`
                  <button type="button" class="pill" role="radio" data-count="${l.count}" aria-checked="${l.count === selected}">
                    <span class="pill__count">${l.count} câu</span>
                    <span class="pill__meta">~${l.minutes} phút · ${l.label}</span>
                    ${l.recommended ? html`<span class="pill__tag">Khuyến nghị</span>` : ''}
                  </button>
                `,
              )}
            </div>
            <p class="start-card__hint">Nhiều câu hỏi hơn giúp kết quả ổn định hơn, nhất là khi bạn ở gần ranh giới giữa hai xu hướng.</p>
            <button type="button" class="btn btn--primary btn--lg btn--block" data-start>Bắt đầu bài kiểm tra</button>
            ${answered
              ? html`<button type="button" class="btn btn--ghost btn--block" data-resume>
                  Tiếp tục bài đang làm (${answered}/${progress.questions.length})
                </button>`
              : ''}
            ${lastResult
              ? html`<button type="button" class="btn btn--ghost btn--block" data-last>
                  Xem lại kết quả gần nhất · ${lastResult.mbti_type}
                </button>`
              : ''}
          </div>
        </div>
      </section>

      <section class="snap-section" aria-labelledby="dims-title">
        <div class="snap-section__inner container">
          <header class="section__head">
            <p class="eyebrow">Mô hình MBTI</p>
            <h2 id="dims-title">Bốn chiều của tính cách</h2>
            <p class="section__lede">${LANDING.dimsIntro}</p>
          </header>
          <div class="grid grid--4">
            ${DICHOTOMIES.map(
              (d) => html`
                <article class="card dim-card" data-dim="${d.key}">
                  <p class="dim-card__theme">${d.theme}</p>
                  <h3 class="dim-card__pair">
                    <span>${d.key[0]}</span><span class="dim-card__vs">/</span><span>${d.key[1]}</span>
                  </h3>
                  <p class="dim-card__question">${d.question}</p>
                  <ul class="dim-card__poles">
                    ${[...d.key].map(
                      (p) => html`<li>
                        <b class="dim-card__letter">${p}</b><span class="dim-card__sep" aria-hidden="true">–</span><span
                          lang="en">${POLES_EN[p]}</span><span class="dim-card__sep" aria-hidden="true">–</span><span
                          class="dim-card__vi">${POLES[p]}</span>
                      </li>`,
                    )}
                  </ul>
                </article>
              `,
            )}
          </div>
        </div>
      </section>

      <section class="snap-section snap-section--last" aria-labelledby="fn-title">
        <div class="snap-section__inner container">
          <header class="section__head">
            <p class="eyebrow">Tâm lý học Phân tích</p>
            <h2 id="fn-title">Tám chức năng nhận thức</h2>
            <p class="section__lede">${LANDING.functionsIntro}</p>
          </header>
          <div class="grid grid--fn">
            ${FUNCTIONS.map(
              (f) => html`
                <article class="fn-chip" data-family="${f.code[0]}">
                  <span class="fn-chip__code">${f.code}</span>
                  <div class="fn-chip__body">
                    <h3 class="fn-chip__name" lang="en">${f.en}</h3>
                    <p class="fn-chip__vi">${f.vi}</p>
                    <p class="fn-chip__desc">${f.desc}</p>
                  </div>
                </article>
              `,
            )}
          </div>
        </div>
        <footer class="site-footer landing-footer"><p>${FOOTER_NOTE}</p></footer>
      </section>

      <nav class="page-dots" aria-label="Các phần của trang">
        ${LANDING.sections.map(
          (label, i) => html`
            <button type="button" class="page-dots__dot" data-goto="${i}" aria-label="${label}" aria-current="${i === 0}">
              <span class="page-dots__label" aria-hidden="true">${label}</span>
            </button>
          `,
        )}
      </nav>
    `,
  );

  const pills = $$('.pill', root);
  const select = (count) => {
    selected = count;
    pills.forEach((p) => p.setAttribute('aria-checked', String(Number(p.dataset.count) === count)));
  };

  const dots = $$('.page-dots__dot', root);
  const page = createFullPage($$('.snap-section', root), {
    onActive: (i) => dots.forEach((d, j) => d.setAttribute('aria-current', String(i === j))),
  });

  const onClick = (e) => {
    const pill = e.target.closest('.pill');
    if (pill) return select(Number(pill.dataset.count));
    const dot = e.target.closest('[data-goto]');
    if (dot) return page.goTo(Number(dot.dataset.goto));
    if (e.target.closest('[data-start]')) {
      tabState.set(KEYS.progress, null);
      return go('quiz', { count: selected });
    }
    if (e.target.closest('[data-resume]')) return go('quiz', { resume: true });
    if (e.target.closest('[data-last]')) return go('result', { result: lastResult });
  };

  // Radio-group keyboard pattern: arrows move the selection.
  const onKey = (e) => {
    if (!e.target.classList?.contains('pill')) return;
    const i = pills.indexOf(e.target);
    const delta = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
    if (delta === undefined) return;
    e.preventDefault();
    const next = pills[(i + delta + pills.length) % pills.length];
    select(Number(next.dataset.count));
    next.focus();
  };

  root.addEventListener('click', onClick);
  root.addEventListener('keydown', onKey);
  return () => {
    root.removeEventListener('click', onClick);
    root.removeEventListener('keydown', onKey);
    page.destroy();
  };
}
