// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: false },
  ssr: false,
  modules: [],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'Clinic EMR - Electronic Medical Record System',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Clinic Electronic Medical Record System for Doctors' }
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap' }
      ],
      script: [
        {
          src: 'https://cdn.tailwindcss.com',
        },
        {
          innerHTML: `
            tailwind.config = {
              theme: {
                extend: {
                  fontFamily: {
                    sans: ['"Plus Jakarta Sans"', 'ui-sans-serif', 'system-ui', 'sans-serif']
                  },
                  colors: {
                    brand: {
                      50: '#ecfdf5',
                      100: '#d1fae5',
                      200: '#a7f3d0',
                      300: '#6ee7b7',
                      400: '#34d399',
                      500: '#10b981',
                      600: '#059669',
                      700: '#047857',
                      800: '#065f46',
                      900: '#064e3b'
                    },
                    medical: {
                      50: '#f0f9ff',
                      100: '#e0f2fe',
                      200: '#bae6fd',
                      300: '#7dd3fc',
                      400: '#38bdf8',
                      500: '#0ea5e9',
                      600: '#0284c7',
                      700: '#0369a1',
                      800: '#075985',
                      900: '#0c4a6e'
                    }
                  }
                }
              }
            }
          `
        }
      ]
    }
  },
  runtimeConfig: {
    public: {
      // Nuxt automatically overrides this with NUXT_PUBLIC_API_BASE_URL from .env
      apiBaseUrl: 'http://127.0.0.1:8000'
    }
  }
})
