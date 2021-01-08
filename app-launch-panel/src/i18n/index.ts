import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import en from './en.json'
import fr from './fr.json'

const resources = {
  en,
  fr
}

const fallbackLng = 'en'
const availableLanguages = ['en', 'fr']

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    detection: {
      order: ['navigator']
    },
    resources,
    whitelist: availableLanguages,
    nonExplicitWhitelist: true,
    fallbackLng: fallbackLng,
    interpolation: {
      escapeValue: false
    }
  })

export default i18n
