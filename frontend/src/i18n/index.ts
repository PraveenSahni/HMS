import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

import en from './locales/en.json'
import ar from './locales/ar.json'

const savedLang = localStorage.getItem('ist-health-lang') ?? 'en'

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    ar: { translation: ar },
  },
  lng: savedLang,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
})

function applyLocale(lang: 'en' | 'ar') {
  document.documentElement.lang = lang
  document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr'
  document.documentElement.classList.toggle('ist-locale-ar', lang === 'ar')
}

export function setLanguage(lang: 'en' | 'ar') {
  localStorage.setItem('ist-health-lang', lang)
  applyLocale(lang)
  i18n.changeLanguage(lang)
}

applyLocale(savedLang === 'ar' ? 'ar' : 'en')

export default i18n
