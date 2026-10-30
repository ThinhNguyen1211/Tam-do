// Full-page section controller, on top of CSS `scroll-snap-type: y mandatory` (views.css).
//
// - Wheel: one gesture = one section. CSS alone snaps to the point nearest where the scroll
//   would end, so a single ~100px mouse-wheel notch would snap straight back.
// - Sections whose content is taller than the screen scroll internally first; the page only
//   moves on the next gesture after the inner scroll reaches its edge.
// - Touch, keyboard and dot clicks rely on the native mandatory snap, which never rests between
//   sections. (Touch chains from an inner scroller to the page at its edge, then snaps.)
// - Reports the active section via IntersectionObserver (for the dot navigation).

const QUIET_MS = 200; // a new gesture starts after this much wheel silence (absorbs trackpad inertia)
const SETTLE_FALLBACK_MS = 900; // for browsers without the `scrollend` event

/**
 * @param {HTMLElement[]} sections  full-viewport snap sections, top to bottom
 * @param {{ onActive?: (index: number) => void }} [options]
 * @returns {{ goTo: (index: number) => void, destroy: () => void }}
 */
export function createFullPage(sections, { onActive } = {}) {
  let animating = false;
  let quietUntil = 0;
  let settleTimer = null;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');

  // The sticky header height (tokens.css); also the page's scroll-padding-top on the landing view.
  const headerOffset = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 0;
  const topOf = (s) => Math.max(0, Math.round(s.getBoundingClientRect().top + scrollY - headerOffset()));
  // Index of the section the page is snapped to (nearest snap position).
  const currentIndex = () => {
    let best = 0;
    sections.forEach((s, i) => {
      if (Math.abs(topOf(s) - scrollY) < Math.abs(topOf(sections[best]) - scrollY)) best = i;
    });
    return best;
  };
  const canScrollInside = (el, dy) =>
    dy > 0 ? el.scrollTop + el.clientHeight < el.scrollHeight - 1 : el.scrollTop > 0;

  const settle = () => {
    animating = false;
    clearTimeout(settleTimer);
  };

  /** Scrolls to section `index`; `fromBelow` starts it at its end, so upward reading continues. */
  function goTo(index, fromBelow = false) {
    const target = sections[index];
    if (!target) return;
    target.scrollTop = fromBelow ? target.scrollHeight : 0;
    animating = true;
    scrollTo({ top: topOf(target), behavior: reduceMotion.matches ? 'instant' : 'smooth' });
    clearTimeout(settleTimer);
    settleTimer = setTimeout(settle, SETTLE_FALLBACK_MS);
  }

  const onWheel = (e) => {
    if (e.ctrlKey || Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return; // zoom / horizontal
    const now = performance.now();
    const isNewGesture = !animating && now >= quietUntil;
    quietUntil = now + QUIET_MS;

    const index = currentIndex();
    // Let the browser scroll an overflowing section natively until it reaches its edge.
    if (!animating && canScrollInside(sections[index], e.deltaY)) return;

    e.preventDefault();
    if (!isNewGesture) return;
    const next = index + Math.sign(e.deltaY);
    if (next >= 0 && next < sections.length) goTo(next, next < index);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) onActive?.(sections.indexOf(entry.target));
      }
    },
    // Below the sticky header; a section counts as active once it fills most of the screen.
    { rootMargin: `-${headerOffset()}px 0px 0px 0px`, threshold: 0.6 },
  );
  sections.forEach((s) => observer.observe(s));

  addEventListener('wheel', onWheel, { passive: false });
  addEventListener('scrollend', settle);
  return {
    goTo: (index) => goTo(index),
    destroy() {
      removeEventListener('wheel', onWheel);
      removeEventListener('scrollend', settle);
      observer.disconnect();
      clearTimeout(settleTimer);
    },
  };
}
