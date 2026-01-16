<script setup lang="ts">
import { ref } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const toast = useToast()

const activeTab = ref('geral')

// Profile
const profileName = ref(authStore.userName)
const profileEmail = ref(authStore.userEmail)

// Notifications
const notifications = ref({
  email: true,
  browser: false,
  faturaProcessada: true,
  erros: true
})

// API Keys (masked)
const apiKeys = ref({
  gemini: '••••••••••••••••',
  sheetsId: '••••••••••••••••'
})

function saveProfile() {
  toast.success('Perfil atualizado com sucesso!')
}

function saveNotifications() {
  toast.success('Notificações atualizadas!')
}

function regenerateKey(key: string) {
  toast.info(`Chave ${key} será regenerada em produção`)
}
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Configurações</h1>
      <p class="text-gray-500 dark:text-gray-400 mt-1">Gerencie as configurações do sistema</p>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200 dark:border-gray-700">
      <nav class="flex gap-8">
        <button 
          v-for="tab in [
            { id: 'geral', name: 'Geral' },
            { id: 'perfil', name: 'Perfil' },
            { id: 'notificacoes', name: 'Notificações' },
            { id: 'integracao', name: 'Integrações' }
          ]"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="py-4 text-sm font-medium border-b-2 transition-colors"
          :class="[
            activeTab === tab.id 
              ? 'border-primary-500 text-primary-600 dark:text-primary-400' 
              : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
          ]"
        >
          {{ tab.name }}
        </button>
      </nav>
    </div>

    <!-- Tab Content -->
    <div class="bg-white dark:bg-dark-200 rounded-2xl border border-gray-100 dark:border-gray-800">
      <!-- Geral -->
      <div v-if="activeTab === 'geral'" class="p-6 space-y-6">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Aparência</h3>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-100 rounded-xl">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">Tema</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">Escolha entre claro, escuro ou sistema</p>
              </div>
              <div class="flex items-center gap-2">
                <button 
                  @click="themeStore.setTheme('light')"
                  class="p-2 rounded-lg transition-colors"
                  :class="!themeStore.isDark ? 'bg-primary-500 text-white' : 'bg-gray-200 dark:bg-dark-200 text-gray-600 dark:text-gray-400'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                </button>
                <button 
                  @click="themeStore.setTheme('dark')"
                  class="p-2 rounded-lg transition-colors"
                  :class="themeStore.isDark ? 'bg-primary-500 text-white' : 'bg-gray-200 dark:bg-dark-200 text-gray-600 dark:text-gray-400'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Idioma</h3>
          <select class="input-field !w-auto">
            <option value="pt-BR">Português (Brasil)</option>
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
        </div>
      </div>

      <!-- Perfil -->
      <div v-if="activeTab === 'perfil'" class="p-6 space-y-6">
        <div class="flex items-center gap-6">
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-2xl font-bold">
            {{ authStore.userName.charAt(0).toUpperCase() }}
          </div>
          <div>
            <button class="btn-secondary text-sm">Alterar foto</button>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input v-model="profileName" label="Nome completo" placeholder="Seu nome" />
          <Input v-model="profileEmail" label="Email" type="email" placeholder="seu@email.com" disabled />
        </div>
        
        <div class="pt-4">
          <Button @click="saveProfile">Salvar alterações</Button>
        </div>
      </div>

      <!-- Notificações -->
      <div v-if="activeTab === 'notificacoes'" class="p-6 space-y-6">
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-100 rounded-xl">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">Notificações por email</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">Receber atualizações por email</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notifications.email" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-100 rounded-xl">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">Fatura processada</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">Notificar quando uma fatura for processada</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notifications.faturaProcessada" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-100 rounded-xl">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">Alertas de erro</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">Notificar quando houver erros no processamento</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notifications.erros" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
        
        <div class="pt-4">
          <Button @click="saveNotifications">Salvar preferências</Button>
        </div>
      </div>

      <!-- Integrações -->
      <div v-if="activeTab === 'integracao'" class="p-6 space-y-6">
        <div class="space-y-4">
          <!-- Google -->
          <div class="p-4 bg-gray-50 dark:bg-dark-100 rounded-xl">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-white dark:bg-dark-200 flex items-center justify-center">
                  <svg class="w-6 h-6" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-gray-900 dark:text-white">Google (Gmail, Drive, Sheets)</p>
                  <p class="text-sm text-green-600 flex items-center gap-1">
                    <span class="w-2 h-2 rounded-full bg-green-500"></span>
                    Conectado
                  </p>
                </div>
              </div>
              <Button variant="secondary" size="sm">Reconectar</Button>
            </div>
          </div>
          
          <!-- Gemini API -->
          <div class="p-4 bg-gray-50 dark:bg-dark-100 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-gray-900 dark:text-white">Google Gemini API</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Extração de dados com IA</p>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <input type="text" :value="apiKeys.gemini" disabled class="input-field flex-1 !py-2 font-mono text-sm" />
              <Button variant="secondary" size="sm" @click="regenerateKey('gemini')">Regenerar</Button>
            </div>
          </div>
        </div>
        
        <div class="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-4 border border-blue-100 dark:border-blue-800">
          <p class="text-sm text-blue-800 dark:text-blue-400">
            <strong>Nota:</strong> As chaves de API são gerenciadas nas variáveis de ambiente do Vercel para maior segurança.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
