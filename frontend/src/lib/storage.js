// Browser storage can be missing or throw (private mode, blocked site data), so every
// access is wrapped and the app works without it.

function read(store, key) {
  try {
    const v = store().getItem(key);
    return v == null ? null : JSON.parse(v);
  } catch {
    return null;
  }
}

function write(store, key, value) {
  try {
    if (value == null) store().removeItem(key);
    else store().setItem(key, JSON.stringify(value));
  } catch {
    /* storage unavailable: degrade silently */
  }
}

const local = () => window.localStorage;
const session = () => window.sessionStorage;

export const KEYS = {
  theme: 'tamdo-theme',
  lastResult: 'tamdo-last-result',
  progress: 'tamdo-progress',
};

export const prefs = { get: (k) => read(local, k), set: (k, v) => write(local, k, v) };
// In-progress answers live in sessionStorage: they survive a reload but not closing the tab.
export const tabState = { get: (k) => read(session, k), set: (k, v) => write(session, k, v) };
