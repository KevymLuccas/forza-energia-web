<script setup lang="ts">
import { ref } from 'vue'
import { useFaturasStore } from '@/stores/faturas'
import { useToast } from 'vue-toastification'
import Button from '@/components/ui/Button.vue'

const faturasStore = useFaturasStore()
const toast = useToast()

const loading = ref(false)
const lastSync = ref<string | null>(null)
const emailStats = ref({
  total: 0,
  novos: 0,
  processados: 0
})

async function baixarFaturas() {
  loading.value = true
  const result = await faturasStore.baixarDoGmail()
  loading.value = false
  
  if (result.success) {
    toast.success('Faturas baixadas com sucesso!')
    lastSync.value = new Date().toLocaleString('pt-BR')
    emailStats.value = {
      total: result.data?.total || 0,
      novos: result.data?.novos || 0,
      processados: result.data?.processados || 0
    }
  } else {
    toast.error(result.error || 'Erro ao baixar faturas')
  }
}

async function processarTodas() {
  loading.value = true
  const result = await faturasStore.processarTodas()
  loading.value = false
  
  if (result.success) {
    toast.success('Faturas processadas com sucesso!')
  } else {
    toast.error(result.error || 'Erro ao processar faturas')
  }
}
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Integração Gmail</h1>
      <p class="text-gray-500 dark:text-gray-400 mt-1">Baixe faturas automaticamente do seu Gmail</p>
    </div>

    <!-- Connection Status -->
    <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-2xl bg-red-500/10 flex items-center justify-center">
            <svg class="w-8 h-8 text-red-500" viewBox="0 0 24 24">
              <path fill="currentColor" d="M20 18h-2V9.25L12 13 6 9.25V18H4V6h1.2l6.8 4.25L18.8 6H20v12M20 4H4c-1.11 0-2 .89-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/>
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900 dark:text-white">Gmail Conectado</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Última sincronização: {{ lastSync || 'Nunca' }}
            </p>
          </div>
        </div>
        
        <div class="flex items-center gap-2">
          <span class="flex items-center gap-1.5 text-sm text-green-600 dark:text-green-400">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Conectado
          </span>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Baixar Faturas -->
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900 dark:text-white">Baixar Faturas</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Busca emails com assunto "Fatura"</p>
          </div>
        </div>
        
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Busca automaticamente todos os emails com faturas de energia em anexo (PDF) que ainda não foram processados.
        </p>
        
        <Button @click="baixarFaturas" :loading="loading" block>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Baixar do Gmail
        </Button>
      </div>

      <!-- Processar Todas -->
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-12 h-12 rounded-xl bg-primary-500/10 flex items-center justify-center">
            <svg class="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900 dark:text-white">Processar Todas</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Extrai dados + Upload Drive</p>
          </div>
        </div>
        
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Processa todas as faturas baixadas: descriptografa PDFs, extrai dados com IA e faz upload organizado no Drive.
        </p>
        
        <Button @click="processarTodas" :loading="loading" block>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Processar Tudo
        </Button>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800 text-center">
        <p class="text-4xl font-bold text-gray-900 dark:text-white mb-2">{{ emailStats.total }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400">Emails encontrados</p>
      </div>
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800 text-center">
        <p class="text-4xl font-bold text-blue-600 mb-2">{{ emailStats.novos }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400">Novas faturas</p>
      </div>
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800 text-center">
        <p class="text-4xl font-bold text-green-600 mb-2">{{ emailStats.processados }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400">Processados</p>
      </div>
    </div>

    <!-- Configuration Info -->
    <div class="bg-yellow-50 dark:bg-yellow-900/20 rounded-2xl p-6 border border-yellow-100 dark:border-yellow-800">
      <div class="flex gap-4">
        <div class="w-10 h-10 rounded-xl bg-yellow-500/20 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-yellow-900 dark:text-yellow-300 mb-2">Configuração Necessária</h3>
          <p class="text-sm text-yellow-800 dark:text-yellow-400">
            Para que a integração funcione, certifique-se de que as credenciais do Gmail estão configuradas nas variáveis de ambiente do Vercel.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
