import { logo } from '../components/logo.js';
import { POLES, PROFILE_TABS } from '../lib/content.js';
import { $, $$, html, render } from '../lib/dom.js';
import { KEYS, prefs } from '../lib/storage.js';

// Same bands as the backend's per-dimension clarity, applied to the mean distance from 50%.
const CLARITY = [
  [5, 'Nhẹ'],
  [15, 'Vừa phải'],
  [25, 'Rõ ràng'],
  [50, 'Rất rõ ràng'],
];
const STRENGTH = [100, 72, 48, 28]; // visual weight of each stack position

function overallClarity(pcts) {
  const mean = ['E', 'S', 'T', 'J'].reduce((s, k) => s + Math.abs(pcts[k] - 50), 0) / 4;
  return CLARITY.find(([bound]) => mean <= bound)[1];
}

function shareText(r) {
  const p = r.percentages;
  return [
    `Kết quả trắc nghiệm tính cách của tôi: ${r.mbti_type} — ${r.type_title}`,
    `“${r.tagline}”`,
    `E ${p.E}% · I ${p.I}% | S ${p.S}% · N ${p.N}% | T ${p.T}% · F ${p.F}% | J ${p.J}% · P ${p.P}%`,
    `Làm bài miễn phí tại ${location.origin}`,
  ].join('\n');
}

const dimensionBars = (r) => html`
  <ul class="bars">
    ${r.dimensions.map((d) => {
      const [a, b] = d.dichotomy;
      const pa = r.percentages[a];
      const pb = r.percentages[b];
      return html`
        <li class="bar" data-dim="${d.dichotomy}">
          <div class="bar__labels">
            <span class="${d.preferred === a ? 'is-preferred' : ''}"><b>${a}</b> ${POLES[a]} <span class="bar__pct">${pa}%</span></span>
            <span class="${d.preferred === b ? 'is-preferred' : ''}"><span class="bar__pct">${pb}%</span> ${POLES[b]} <b>${b}</b></span>
          </div>
          <div class="bar__track" role="img" aria-label="${POLES[a]} ${pa}%, ${POLES[b]} ${pb}%">
            <span class="bar__seg ${d.preferred === a ? 'is-preferred' : ''}" data-pct="${pa}"></span>
            <span class="bar__seg ${d.preferred === b ? 'is-preferred' : ''}" data-pct="${pb}"></span>
            <span class="bar__mid" aria-hidden="true"></span>
          </div>
          <p class="bar__note"><span class="chip" data-clarity="${d.clarity}">${d.clarity_label}</span> ${d.note}</p>
        </li>
      `;
    })}
  </ul>
`;

const functionStack = (stack) => html`
  <ol class="stack">
    ${stack.map(
      (f, i) => html`
        <li class="stack__item" data-family="${f.function[0]}">
          <span class="stack__code">${f.function}</span>
          <div class="stack__body">
            <p class="stack__pos">${f.position} <span lang="en">· ${f.position_en}</span></p>
            <h3 class="stack__name">${f.name}</h3>
            <div class="stack__meter" aria-hidden="true"><span data-pct="${STRENGTH[i]}"></span></div>
            <p class="stack__role">${f.role}</p>
            <p class="stack__desc">${f.description}</p>
          </div>
        </li>
      `,
    )}
  </ol>
`;

function sectionBody(key, s) {
  if (key === 'strengths_growth') {
    return html`
      <p>${s.content}</p>
      <div class="two-col">
        <div class="list-card list-card--strengths">
          <h4>Điểm mạnh tự nhiên</h4>
          <ul>${s.strengths.map((x) => html`<li>${x}</li>`)}</ul>
        </div>
        <div class="list-card list-card--growth">
          <h4>Hướng phát triển</h4>
          <ul>${s.growth_areas.map((x) => html`<li>${x}</li>`)}</ul>
        </div>
      </div>
    `;
  }
  return html`<p>${s.content}</p>`;
}

export function resultView(root, { result: r }, go) {
  if (!r) {
    // Defer so the router finishes mounting this view before switching away.
    queueMicrotask(() => go('landing'));
    return;
  }
  const profile = r.psychological_profile;
  const stack = profile.cognitive_functions.function_stack;
  const canShare = typeof navigator.share === 'function';

  render(
    root,
    html`
      <section class="container result">
        <header class="card card--glass result-hero">
          <div class="result-hero__logo">${logo('logo--result')}</div>
          <p class="eyebrow">Kiểu tính cách của bạn</p>
          <h1 class="result-hero__type" tabindex="-1" data-autofocus aria-label="${r.mbti_type}: ${r.type_title}">
            ${[...r.mbti_type].map((ch, i) => html`<span class="type-letter" data-dim="${['EI', 'SN', 'TF', 'JP'][i]}" title="${POLES[ch]}">${ch}</span>`)}
          </h1>
          <p class="result-hero__title">${r.type_title_vi} <span lang="en">· ${r.type_title_en}</span></p>
          <p class="result-hero__tagline">${r.tagline}</p>
          <p class="badge">Độ rõ ràng tổng thể: <strong>${overallClarity(r.percentages)}</strong></p>
          <div class="result-actions">
            <button type="button" class="btn btn--primary" data-export>Tải kết quả / Chia sẻ</button>
            <button type="button" class="btn btn--ghost" data-retake>Làm lại bài test</button>
          </div>
        </header>

        <div class="result-grid">
          <section class="card panel" aria-labelledby="bars-title">
            <h2 id="bars-title" class="panel__title">Phổ xu hướng</h2>
            <p class="panel__lede">Tỷ lệ phần trăm cho thấy mức độ bạn nghiêng về mỗi phía, không phải năng lực.</p>
            ${dimensionBars(r)}
          </section>
          <section class="card panel" aria-labelledby="stack-title">
            <h2 id="stack-title" class="panel__title">Ngăn xếp chức năng nhận thức</h2>
            <p class="panel__lede">Thứ tự Jung–Myers: chức năng chủ đạo dẫn đường, chức năng tiềm ẩn là vùng trưởng thành.</p>
            ${functionStack(stack)}
          </section>
        </div>

        <section class="card panel profile" aria-labelledby="profile-title">
          <h2 id="profile-title" class="panel__title">Hồ sơ tâm lý chi tiết</h2>
          <div class="tabs" role="tablist" aria-labelledby="profile-title">
            ${PROFILE_TABS.map(
              ([key, label], i) => html`
                <button type="button" class="tab" role="tab" id="tab-${key}" aria-controls="panel-${key}"
                  aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}">
                  <span class="tab__num">0${i + 1}</span> ${label}
                </button>
              `,
            )}
          </div>
          ${PROFILE_TABS.map(
            ([key, label, labelEn], i) => html`
              <div class="tabpanel" role="tabpanel" id="panel-${key}" aria-labelledby="tab-${key}" tabindex="0" ${i === 0 ? '' : html`hidden`}>
                <h3 class="tabpanel__title">${label} <span lang="en">· ${labelEn}</span></h3>
                ${sectionBody(key, profile[key])}
              </div>
            `,
          )}
        </section>

        <p class="disclaimer">${r.disclaimer}</p>
      </section>

      <dialog class="dialog card card--glass" data-dialog aria-labelledby="dlg-title">
        <h2 id="dlg-title">Lưu & chia sẻ kết quả</h2>
        <div class="dialog__actions">
          <button type="button" class="btn btn--primary btn--block" data-print>Lưu thành PDF / In</button>
          ${canShare ? html`<button type="button" class="btn btn--ghost btn--block" data-share>Chia sẻ…</button>` : ''}
          <button type="button" class="btn btn--ghost btn--block" data-copy>Sao chép tóm tắt</button>
        </div>
        <p class="dialog__status" data-status role="status"></p>
        <button type="button" class="link-btn" data-close>Đóng</button>
      </dialog>
    `,
  );

  const tabs = $$('.tab', root);
  const panels = $$('.tabpanel', root);
  const dialog = $('[data-dialog]', root);
  const status = $('[data-status]', root);

  function selectTab(i, focus = true) {
    tabs.forEach((t, j) => {
      t.setAttribute('aria-selected', String(i === j));
      t.tabIndex = i === j ? 0 : -1;
      panels[j].hidden = i !== j;
    });
    if (focus) tabs[i].focus();
  }

  const onClick = async (e) => {
    const tab = e.target.closest('.tab');
    if (tab) return selectTab(tabs.indexOf(tab));
    if (e.target.closest('[data-retake]')) return go('landing');
    if (e.target.closest('[data-export]')) {
      status.textContent = '';
      return dialog.showModal();
    }
    if (e.target.closest('[data-close]')) return dialog.close();
    if (e.target.closest('[data-print]')) {
      dialog.close();
      return window.print();
    }
    if (e.target.closest('[data-share]')) {
      try {
        await navigator.share({ title: `${r.mbti_type} — ${r.type_title}`, text: shareText(r), url: location.origin });
        dialog.close();
      } catch {
        /* user cancelled the share sheet */
      }
      return;
    }
    if (e.target.closest('[data-copy]')) {
      try {
        await navigator.clipboard.writeText(shareText(r));
        status.textContent = 'Đã sao chép vào bộ nhớ tạm.';
      } catch {
        status.textContent = 'Trình duyệt không cho phép sao chép tự động.';
      }
    }
  };

  // WAI-ARIA tabs pattern: arrows / Home / End move between tabs.
  const onKey = (e) => {
    const i = tabs.indexOf(e.target);
    if (i < 0) return;
    const next = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
    if (next === undefined) return;
    e.preventDefault();
    selectTab((next + tabs.length) % tabs.length);
  };

  root.addEventListener('click', onClick);
  root.addEventListener('keydown', onKey);
  prefs.set(KEYS.lastResult, r);
  return () => {
    root.removeEventListener('click', onClick);
    root.removeEventListener('keydown', onKey);
  };
}
