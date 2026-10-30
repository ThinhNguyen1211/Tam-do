import { KEYS, prefs } from './storage.js';

const META_COLOR = { dark: '#0b1020', light: '#f6f5f1' };

export const getTheme = () => (document.documentElement.dataset.theme === 'light' ? 'light' : 'dark');

export function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', META_COLOR[theme]);
  prefs.set(KEYS.theme, theme);
}

export const toggleTheme = () => setTheme(getTheme() === 'dark' ? 'light' : 'dark');
