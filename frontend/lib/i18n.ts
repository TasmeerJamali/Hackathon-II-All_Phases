/**
 * Internationalization (i18n) Configuration
 * 
 * Supports: English (en), Urdu (ur)
 * Features: RTL support, language toggle, localStorage persistence
 */

import en from '../locales/en.json';
import ur from '../locales/ur.json';

export type Locale = 'en' | 'ur';

export interface I18nConfig {
  locale: Locale;
  direction: 'ltr' | 'rtl';
  translations: typeof en;
}

const translations: Record<Locale, typeof en> = {
  en,
  ur,
};

const rtlLocales: Locale[] = ['ur'];

export function getDirection(locale: Locale): 'ltr' | 'rtl' {
  return rtlLocales.includes(locale) ? 'rtl' : 'ltr';
}

export function getTranslations(locale: Locale): typeof en {
  return translations[locale] || translations.en;
}

export function t(locale: Locale, key: string): string {
  const keys = key.split('.');
  let value: unknown = translations[locale];
  
  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = (value as Record<string, unknown>)[k];
    } else {
      // Fallback to English
      value = translations.en;
      for (const fallbackKey of keys) {
        if (value && typeof value === 'object' && fallbackKey in value) {
          value = (value as Record<string, unknown>)[fallbackKey];
        } else {
          return key; // Return key if not found
        }
      }
      break;
    }
  }
  
  return typeof value === 'string' ? value : key;
}

export function getStoredLocale(): Locale {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('locale');
    if (stored === 'en' || stored === 'ur') {
      return stored;
    }
  }
  return 'en';
}

export function setStoredLocale(locale: Locale): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('locale', locale);
    // Update document direction
    document.documentElement.dir = getDirection(locale);
    document.documentElement.lang = locale;
  }
}

export const localeNames: Record<Locale, string> = {
  en: 'English',
  ur: 'اردو',
};

export const supportedLocales: Locale[] = ['en', 'ur'];
