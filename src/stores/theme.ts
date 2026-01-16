import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useStorage } from '@vueuse/core'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)
  const storedTheme = useStorage('forza-theme', 'light')

  function initTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDark.value = storedTheme.value === 'dark' || (storedTheme.value === 'system' && prefersDark)
    applyTheme()
  }

  function toggleTheme() {
    isDark.value = !isDark.value
    storedTheme.value = isDark.value ? 'dark' : 'light'
    applyTheme()
  }

  function setTheme(theme: 'light' | 'dark' | 'system') {
    storedTheme.value = theme
    if (theme === 'system') {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    } else {
      isDark.value = theme === 'dark'
    }
    applyTheme()
  }

  function applyTheme() {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    isDark,
    storedTheme,
    initTheme,
    toggleTheme,
    setTheme
  }
})
