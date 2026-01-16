<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useFaturasStore } from '@/stores/faturas'
import StatsCard from '@/components/ui/StatsCard.vue'
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const faturasStore = useFaturasStore()

onMounted(() => {
  faturasStore.fetchFaturas()
})

const stats = computed(() => faturasStore.getStats())

// Chart Data
const lineChartData = computed(() => ({
  labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
  datasets: [
    {
      label: 'Consumo kWh',
      data: [320, 450, 380, 520, 410, 480],
      borderColor: '#22c55e',
      backgroundColor: 'rgba(34, 197, 94, 0.1)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#22c55e',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6
    }
  ]
}))

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 12,
      cornerRadius: 8,
      displayColors: false
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        color: '#9ca3af'
      }
    },
    y: {
      grid: {
        color: 'rgba(156, 163, 175, 0.1)'
      },
      ticks: {
        color: '#9ca3af'
      }
    }
  }
}

const doughnutChartData = computed(() => ({
  labels: ['Concluídas', 'Pendentes', 'Processando', 'Erros'],
  datasets: [
    {
      data: [stats.value.concluidas, stats.value.pendentes, stats.value.processando, stats.value.erros],
      backgroundColor: ['#22c55e', '#eab308', '#3b82f6', '#ef4444'],
      borderWidth: 0,
      cutout: '75%'
    }
  ]
}))

const doughnutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 20,
        usePointStyle: true,
        pointStyle: 'circle',
        color: '#9ca3af'
      }
    }
  }
}

// Recent faturas
const recentFaturas = computed(() => faturasStore.faturas.slice(0, 5))

function formatCurrency(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('pt-BR')
}
</script>

<template>
  <div class="space-y-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p class="text-gray-500 dark:text-gray-400 mt-1">Visão geral das suas faturas de energia</p>
      </div>
      
      <div class="flex items-center gap-3">
        <select class="input-field !w-auto !py-2.5 text-sm">
          <option>Últimos 30 dias</option>
          <option>Últimos 60 dias</option>
          <option>Últimos 90 dias</option>
          <option>Este ano</option>
        </select>
        
        <router-link 
          to="/upload"
          class="btn-primary !py-2.5 flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nova Fatura
        </router-link>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatsCard 
        title="Total de Faturas" 
        :value="stats.total"
        icon="document"
        color="blue"
        :trend="12"
        trend-label="vs mês anterior"
      />
      <StatsCard 
        title="Valor Total" 
        :value="formatCurrency(stats.valorTotal)"
        icon="money"
        color="green"
        :trend="-5"
        trend-label="vs mês anterior"
      />
      <StatsCard 
        title="Consumo Total" 
        :value="`${stats.consumoTotal.toLocaleString('pt-BR')} kWh`"
        icon="bolt"
        color="yellow"
        :trend="8"
        trend-label="vs mês anterior"
      />
      <StatsCard 
        title="Processadas" 
        :value="stats.concluidas"
        icon="check"
        color="green"
      />
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Line Chart -->
      <div class="lg:col-span-2 bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Consumo Mensal</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Evolução do consumo em kWh</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-primary-500"></span>
            <span class="text-sm text-gray-500 dark:text-gray-400">kWh</span>
          </div>
        </div>
        <div class="h-72">
          <Line :data="lineChartData" :options="lineChartOptions" />
        </div>
      </div>

      <!-- Doughnut Chart -->
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Status das Faturas</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">Distribuição por status</p>
        </div>
        <div class="h-64">
          <Doughnut :data="doughnutChartData" :options="doughnutChartOptions" />
        </div>
      </div>
    </div>

    <!-- Recent Faturas Table -->
    <div class="bg-white dark:bg-dark-200 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
      <div class="p-6 border-b border-gray-100 dark:border-gray-800">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Faturas Recentes</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Últimas faturas processadas</p>
          </div>
          <router-link 
            to="/faturas"
            class="text-sm text-primary-600 hover:text-primary-500 font-medium flex items-center gap-1"
          >
            Ver todas
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-dark-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Cliente</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">UC</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Vencimento</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Consumo</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Valor</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr v-for="fatura in recentFaturas" :key="fatura.id" class="hover:bg-gray-50 dark:hover:bg-dark-100 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-primary-500/10 flex items-center justify-center">
                    <span class="text-primary-600 font-semibold">{{ fatura.numeroCliente?.slice(0, 2) }}</span>
                  </div>
                  <span class="font-medium text-gray-900 dark:text-white">{{ fatura.numeroCliente }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ fatura.unidadeConsumidora }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ fatura.vencimento }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ fatura.consumoKwh?.toLocaleString('pt-BR') }} kWh</td>
              <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{{ formatCurrency(fatura.totalPagar || 0) }}</td>
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
            </tr>
            
            <!-- Empty State -->
            <tr v-if="recentFaturas.length === 0">
              <td colspan="6" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center">
                  <div class="w-16 h-16 rounded-2xl bg-gray-100 dark:bg-dark-100 flex items-center justify-center mb-4">
                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <p class="text-gray-500 dark:text-gray-400 font-medium">Nenhuma fatura encontrada</p>
                  <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">Faça upload de uma fatura para começar</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
