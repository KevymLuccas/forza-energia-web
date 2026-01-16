<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useFaturasStore, type Fatura } from '@/stores/faturas'
import Button from '@/components/ui/Button.vue'

const faturasStore = useFaturasStore()
const searchQuery = ref('')
const statusFilter = ref('todos')
const sortBy = ref('vencimento')
const sortOrder = ref<'asc' | 'desc'>('desc')
const selectedFatura = ref<Fatura | null>(null)
const showModal = ref(false)

onMounted(() => {
  faturasStore.fetchFaturas()
})

const filteredFaturas = computed(() => {
  let result = [...faturasStore.faturas]
  
  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(f => 
      f.numeroCliente?.toLowerCase().includes(query) ||
      f.unidadeConsumidora?.toLowerCase().includes(query)
    )
  }
  
  // Filter by status
  if (statusFilter.value !== 'todos') {
    result = result.filter(f => f.status === statusFilter.value)
  }
  
  // Sort
  result.sort((a, b) => {
    let aVal: any = a[sortBy.value as keyof Fatura]
    let bVal: any = b[sortBy.value as keyof Fatura]
    
    if (sortBy.value === 'vencimento' || sortBy.value === 'createdAt') {
      aVal = new Date(aVal || 0).getTime()
      bVal = new Date(bVal || 0).getTime()
    }
    
    if (sortOrder.value === 'asc') {
      return aVal > bVal ? 1 : -1
    }
    return aVal < bVal ? 1 : -1
  })
  
  return result
})

function openModal(fatura: Fatura) {
  selectedFatura.value = fatura
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedFatura.value = null
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value || 0)
}

function toggleSort(field: string) {
  if (sortBy.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value = field
    sortOrder.value = 'desc'
  }
}
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Faturas</h1>
        <p class="text-gray-500 dark:text-gray-400 mt-1">Gerencie todas as suas faturas de energia</p>
      </div>
      
      <router-link to="/upload">
        <Button>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nova Fatura
        </Button>
      </router-link>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-dark-200 rounded-2xl p-4 border border-gray-100 dark:border-gray-800">
      <div class="flex flex-col lg:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1 relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por cliente ou UC..."
            class="input-field !pl-10"
          />
        </div>
        
        <!-- Status Filter -->
        <select v-model="statusFilter" class="input-field !w-auto">
          <option value="todos">Todos os status</option>
          <option value="concluido">Concluído</option>
          <option value="pendente">Pendente</option>
          <option value="processando">Processando</option>
          <option value="erro">Erro</option>
        </select>
        
        <!-- Sort -->
        <select v-model="sortBy" class="input-field !w-auto">
          <option value="vencimento">Ordenar por vencimento</option>
          <option value="totalPagar">Ordenar por valor</option>
          <option value="consumoKwh">Ordenar por consumo</option>
          <option value="createdAt">Ordenar por data</option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white dark:bg-dark-200 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-dark-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                <button @click="toggleSort('numeroCliente')" class="flex items-center gap-1 hover:text-gray-700">
                  Cliente
                  <svg v-if="sortBy === 'numeroCliente'" class="w-4 h-4" :class="{ 'rotate-180': sortOrder === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">UC</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                <button @click="toggleSort('vencimento')" class="flex items-center gap-1 hover:text-gray-700">
                  Vencimento
                  <svg v-if="sortBy === 'vencimento'" class="w-4 h-4" :class="{ 'rotate-180': sortOrder === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                <button @click="toggleSort('consumoKwh')" class="flex items-center gap-1 hover:text-gray-700">
                  Consumo
                  <svg v-if="sortBy === 'consumoKwh'" class="w-4 h-4" :class="{ 'rotate-180': sortOrder === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                <button @click="toggleSort('totalPagar')" class="flex items-center gap-1 hover:text-gray-700">
                  Valor
                  <svg v-if="sortBy === 'totalPagar'" class="w-4 h-4" :class="{ 'rotate-180': sortOrder === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr 
              v-for="fatura in filteredFaturas" 
              :key="fatura.id" 
              class="hover:bg-gray-50 dark:hover:bg-dark-100 transition-colors cursor-pointer"
              @click="openModal(fatura)"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-primary-500/10 flex items-center justify-center">
                    <span class="text-primary-600 font-semibold text-sm">{{ fatura.numeroCliente?.slice(0, 2) }}</span>
                  </div>
                  <span class="font-medium text-gray-900 dark:text-white">{{ fatura.numeroCliente }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ fatura.unidadeConsumidora }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ fatura.vencimento }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ fatura.consumoKwh?.toLocaleString('pt-BR') }} kWh</td>
              <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white">{{ formatCurrency(fatura.totalPagar) }}</td>
              <td class="px-6 py-4">
                <span 
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400': fatura.status === 'concluido',
                    'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400': fatura.status === 'pendente',
                    'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400': fatura.status === 'processando',
                    'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400': fatura.status === 'erro'
                  }"
                >
                  <span 
                    class="w-1.5 h-1.5 rounded-full"
                    :class="{
                      'bg-green-500': fatura.status === 'concluido',
                      'bg-yellow-500': fatura.status === 'pendente',
                      'bg-blue-500': fatura.status === 'processando',
                      'bg-red-500': fatura.status === 'erro'
                    }"
                  ></span>
                  {{ fatura.status === 'concluido' ? 'Concluído' : fatura.status === 'pendente' ? 'Pendente' : fatura.status === 'processando' ? 'Processando' : 'Erro' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button 
                  class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-100 transition-colors"
                  @click.stop="openModal(fatura)"
                >
                  <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </td>
            </tr>
            
            <!-- Empty State -->
            <tr v-if="filteredFaturas.length === 0">
              <td colspan="7" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center">
                  <div class="w-16 h-16 rounded-2xl bg-gray-100 dark:bg-dark-100 flex items-center justify-center mb-4">
                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <p class="text-gray-500 dark:text-gray-400 font-medium">Nenhuma fatura encontrada</p>
                  <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">Tente ajustar os filtros ou faça upload de uma nova fatura</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div 
          v-if="showModal" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
          @click="closeModal"
        >
          <div 
            class="bg-white dark:bg-dark-200 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
            @click.stop
          >
            <!-- Header -->
            <div class="sticky top-0 bg-white dark:bg-dark-200 p-6 border-b border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">Detalhes da Fatura</h2>
                <p class="text-sm text-gray-500">Cliente: {{ selectedFatura?.numeroCliente }}</p>
              </div>
              <button 
                @click="closeModal"
                class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-100 transition-colors"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <!-- Content -->
            <div class="p-6 space-y-6" v-if="selectedFatura">
              <!-- Main Info -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                  <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Vencimento</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedFatura.vencimento }}</p>
                </div>
                <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                  <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Valor Total</p>
                  <p class="text-lg font-semibold text-green-600">{{ formatCurrency(selectedFatura.totalPagar) }}</p>
                </div>
                <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                  <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Consumo</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedFatura.consumoKwh }} kWh</p>
                </div>
                <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                  <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Dias</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedFatura.diasLeitura }}</p>
                </div>
              </div>
              
              <!-- Leitura -->
              <div>
                <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Dados de Leitura</h3>
                <div class="grid grid-cols-3 gap-4">
                  <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                    <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Leitura Anterior</p>
                    <p class="font-medium text-gray-900 dark:text-white">{{ selectedFatura.leituraAnterior }}</p>
                    <p class="text-xs text-gray-400">{{ selectedFatura.leituraAnteriorData }}</p>
                  </div>
                  <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                    <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Leitura Atual</p>
                    <p class="font-medium text-gray-900 dark:text-white">{{ selectedFatura.leituraAtual }}</p>
                    <p class="text-xs text-gray-400">{{ selectedFatura.leituraAtualData }}</p>
                  </div>
                  <div class="bg-gray-50 dark:bg-dark-100 rounded-xl p-4">
                    <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Próxima Leitura</p>
                    <p class="font-medium text-gray-900 dark:text-white">-</p>
                    <p class="text-xs text-gray-400">{{ selectedFatura.proximaLeituraData }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Energia -->
              <div>
                <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Composição de Valores</h3>
                <div class="space-y-2">
                  <div class="flex justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                    <span class="text-gray-600 dark:text-gray-400">Energia Ativa TE</span>
                    <span class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(selectedFatura.energiaAtivaTE) }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                    <span class="text-gray-600 dark:text-gray-400">Energia Ativa TUSD</span>
                    <span class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(selectedFatura.energiaAtivaTUSD) }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                    <span class="text-gray-600 dark:text-gray-400">Energia Injetada TE</span>
                    <span class="font-medium text-green-600">-{{ formatCurrency(selectedFatura.energiaInjetadaTE) }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                    <span class="text-gray-600 dark:text-gray-400">Energia Injetada TUSD</span>
                    <span class="font-medium text-green-600">-{{ formatCurrency(selectedFatura.energiaInjetadaTUSD) }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                    <span class="text-gray-600 dark:text-gray-400">Iluminação Pública</span>
                    <span class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(selectedFatura.iluminacaoPublica) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
