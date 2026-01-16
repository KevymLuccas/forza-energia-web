<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/layout/Sidebar.vue'
import Navbar from '@/components/layout/Navbar.vue'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const initializing = ref(true)

onMounted(async () => {
  themeStore.initTheme()
  await authStore.checkAuth()
  initializing.value = false
  
  // Se logou e está na página de login, redireciona para dashboard
  if (authStore.isAuthenticated && (route.path === '/login' || route.path === '/register')) {
    router.push('/')
  }
})

// Observa mudanças na autenticação
watch(() => authStore.isAuthenticated, (isAuth) => {
  if (isAuth && (route.path === '/login' || route.path === '/register')) {
    router.push('/')
  }
})

watch(() => themeStore.isDark, (isDark) => {
  document.documentElement.classList.toggle('dark', isDark)
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-300 transition-colors duration-300">
    <!-- Loading -->
    <template v-if="initializing">
      <div class="min-h-screen flex items-center justify-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    </template>

    <!-- Auth Layout -->
    <template v-else-if="!authStore.isAuthenticated">
      <router-view />
    </template>

    <!-- App Layout -->
    <template v-else>
      <div class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <Sidebar />
        
        <!-- Main Content -->
        <div class="flex-1 flex flex-col overflow-hidden">
          <!-- Navbar -->
          <Navbar />
          
          <!-- Page Content -->
          <main class="flex-1 overflow-y-auto p-6 lg:p-8">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </main>
        </div>
      </div>
    </template>
  </div>
</template>
