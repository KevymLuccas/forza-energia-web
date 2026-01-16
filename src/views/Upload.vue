<script setup lang="ts">
import { ref } from 'vue'
import { useFaturasStore } from '@/stores/faturas'
import { useToast } from 'vue-toastification'
import Button from '@/components/ui/Button.vue'

const faturasStore = useFaturasStore()
const toast = useToast()

const isDragging = ref(false)
const files = ref<File[]>([])
const uploading = ref(false)
const uploadProgress = ref<{ [key: string]: number }>({})

function handleDragOver(e: DragEvent) {
  e.preventDefault()
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
  
  const droppedFiles = e.dataTransfer?.files
  if (droppedFiles) {
    addFiles(Array.from(droppedFiles))
  }
}

function handleFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) {
    addFiles(Array.from(input.files))
  }
}

function addFiles(newFiles: File[]) {
  const pdfFiles = newFiles.filter(f => f.type === 'application/pdf')
  if (pdfFiles.length !== newFiles.length) {
    toast.warning('Apenas arquivos PDF são permitidos')
  }
  files.value = [...files.value, ...pdfFiles]
}

function removeFile(index: number) {
  files.value.splice(index, 1)
}

function formatFileSize(bytes: number) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function uploadFiles() {
  if (files.value.length === 0) {
    toast.warning('Selecione pelo menos um arquivo')
    return
  }
  
  uploading.value = true
  let successCount = 0
  let errorCount = 0
  
  for (const file of files.value) {
    uploadProgress.value[file.name] = 0
    
    // Simulate progress
    const interval = setInterval(() => {
      if (uploadProgress.value[file.name] < 90) {
        uploadProgress.value[file.name] += 10
      }
    }, 500)
    
    const result = await faturasStore.uploadFatura(file)
    
    clearInterval(interval)
    uploadProgress.value[file.name] = 100
    
    if (result.success) {
      successCount++
    } else {
      errorCount++
    }
  }
  
  uploading.value = false
  
  if (successCount > 0) {
    toast.success(`${successCount} fatura(s) processada(s) com sucesso!`)
  }
  if (errorCount > 0) {
    toast.error(`${errorCount} fatura(s) com erro no processamento`)
  }
  
  // Clear files after processing
  setTimeout(() => {
    files.value = []
    uploadProgress.value = {}
  }, 2000)
}
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Upload de Faturas</h1>
      <p class="text-gray-500 dark:text-gray-400 mt-1">Faça upload de faturas PDF para extração automática de dados</p>
    </div>

    <!-- Drop Zone -->
    <div 
      class="relative border-2 border-dashed rounded-2xl transition-all duration-300"
      :class="[
        isDragging 
          ? 'border-primary-500 bg-primary-500/5' 
          : 'border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:bg-gray-50 dark:hover:bg-dark-100'
      ]"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
    >
      <input 
        type="file" 
        accept=".pdf"
        multiple
        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        @change="handleFileSelect"
      />
      
      <div class="p-12 text-center">
        <div 
          class="w-20 h-20 mx-auto rounded-2xl flex items-center justify-center mb-6 transition-colors"
          :class="isDragging ? 'bg-primary-500/20' : 'bg-gray-100 dark:bg-dark-100'"
        >
          <svg 
            class="w-10 h-10 transition-colors"
            :class="isDragging ? 'text-primary-500' : 'text-gray-400'"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          {{ isDragging ? 'Solte os arquivos aqui' : 'Arraste e solte seus arquivos PDF' }}
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">ou clique para selecionar</p>
        
        <div class="flex items-center justify-center gap-4 text-sm text-gray-400">
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Somente PDF
          </span>
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
            Máx. 10MB por arquivo
          </span>
        </div>
      </div>
    </div>

    <!-- File List -->
    <div v-if="files.length > 0" class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Arquivos selecionados ({{ files.length }})
        </h3>
        <Button 
          @click="uploadFiles" 
          :loading="uploading"
          :disabled="uploading"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Processar Faturas
        </Button>
      </div>
      
      <div class="bg-white dark:bg-dark-200 rounded-2xl border border-gray-100 dark:border-gray-800 divide-y divide-gray-100 dark:divide-gray-800">
        <div 
          v-for="(file, index) in files" 
          :key="file.name + index"
          class="p-4 flex items-center gap-4"
        >
          <!-- Icon -->
          <div class="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          
          <!-- Info -->
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-900 dark:text-white truncate">{{ file.name }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">{{ formatFileSize(file.size) }}</p>
            
            <!-- Progress Bar -->
            <div v-if="uploadProgress[file.name] !== undefined" class="mt-2">
              <div class="h-1.5 bg-gray-100 dark:bg-dark-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-primary-500 rounded-full transition-all duration-300"
                  :style="{ width: uploadProgress[file.name] + '%' }"
                ></div>
              </div>
            </div>
          </div>
          
          <!-- Status / Remove -->
          <div class="flex-shrink-0">
            <template v-if="uploadProgress[file.name] === 100">
              <div class="w-10 h-10 rounded-xl bg-green-500/10 flex items-center justify-center">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </template>
            <template v-else-if="uploadProgress[file.name] !== undefined">
              <div class="w-10 h-10 rounded-xl bg-primary-500/10 flex items-center justify-center">
                <svg class="w-5 h-5 text-primary-500 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
            </template>
            <template v-else>
              <button 
                @click="removeFile(index)"
                class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-100 transition-colors"
              >
                <svg class="w-5 h-5 text-gray-400 hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- Instructions -->
    <div class="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-6 border border-blue-100 dark:border-blue-800">
      <div class="flex gap-4">
        <div class="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-blue-900 dark:text-blue-300 mb-2">Como funciona</h3>
          <ol class="text-sm text-blue-800 dark:text-blue-400 space-y-1 list-decimal list-inside">
            <li>Faça upload das faturas de energia em PDF</li>
            <li>Nossa IA (Google Gemini) extrai automaticamente todos os dados</li>
            <li>Os dados são salvos na planilha Google Sheets</li>
            <li>O PDF é organizado no Google Drive por data</li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>
