<script setup lang="ts">
import { computed } from 'vue'
import { useFaturasStore } from '@/stores/faturas'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const faturasStore = useFaturasStore()

const stats = computed(() => faturasStore.getStats())

const barChartData = computed(() => ({
  labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
  datasets: [
    {
      label: 'Valor Total (R$)',
      data: [1250, 1480, 1320, 1680, 1420, 1550],
      backgroundColor: 'rgba(34, 197, 94, 0.8)',
      borderRadius: 8,
    },
    {
      label: 'Energia Injetada (R$)',
      data: [450, 520, 480, 620, 510, 580],
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
      borderRadius: 8,
    }
  ]
}))

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        padding: 20,
        usePointStyle: true,
        pointStyle: 'circle',
        color: '#9ca3af'
      }
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
        color: '#9ca3af',
        callback: function(value: any) {
          return 'R$ ' + value
        }
      }
    }
  }
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Relatórios</h1>
        <p class="text-gray-500 dark:text-gray-400 mt-1">Análise detalhada das suas faturas de energia</p>
      </div>
      
      <div class="flex items-center gap-3">
        <select class="input-field !w-auto !py-2.5 text-sm">
          <option>Últimos 6 meses</option>
          <option>Este ano</option>
          <option>Ano passado</option>
        </select>
        
        <button class="btn-secondary !py-2.5 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Exportar PDF
        </button>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center justify-between mb-4">
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Gasto Total</p>
          <span class="text-xs px-2 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">-5%</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(stats.valorTotal) }}</p>
        <p class="text-sm text-gray-500 mt-1">vs período anterior</p>
      </div>
      
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center justify-between mb-4">
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Consumo Total</p>
          <span class="text-xs px-2 py-1 rounded-full bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400">+3%</span>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.consumoTotal.toLocaleString('pt-BR') }} kWh</p>
        <p class="text-sm text-gray-500 mt-1">vs período anterior</p>
      </div>
      
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center justify-between mb-4">
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Média Mensal</p>
        </div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(stats.valorTotal / 6) }}</p>
        <p class="text-sm text-gray-500 mt-1">por mês</p>
      </div>
      
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <div class="flex items-center justify-between mb-4">
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Economia Solar</p>
          <span class="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">Solar</span>
        </div>
        <p class="text-2xl font-bold text-green-600">{{ formatCurrency(3160) }}</p>
        <p class="text-sm text-gray-500 mt-1">energia injetada</p>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Bar Chart -->
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Comparativo Mensal</h3>
        <div class="h-80">
          <Bar :data="barChartData" :options="barChartOptions" />
        </div>
      </div>

      <!-- Top Consumidores -->
      <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 border border-gray-100 dark:border-gray-800">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Top Unidades Consumidoras</h3>
        
        <div class="space-y-4">
          <div v-for="i in 5" :key="i" class="flex items-center gap-4">
            <span class="w-8 h-8 rounded-lg bg-primary-500/10 flex items-center justify-center text-primary-600 font-semibold text-sm">
              {{ i }}
            </span>
            <div class="flex-1">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm font-medium text-gray-900 dark:text-white">UC {{ 1000 + i }}</span>
                <span class="text-sm text-gray-500">{{ 600 - (i * 80) }} kWh</span>
              </div>
              <div class="h-2 bg-gray-100 dark:bg-dark-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
                  :style="{ width: (100 - (i * 15)) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Table -->
    <div class="bg-white dark:bg-dark-200 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
      <div class="p-6 border-b border-gray-100 dark:border-gray-800">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Resumo por Mês</h3>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-dark-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Mês</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Faturas</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Consumo (kWh)</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Injetada (kWh)</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Valor Bruto</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Desconto Solar</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Valor Final</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr v-for="(mes, i) in ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']" :key="mes" class="hover:bg-gray-50 dark:hover:bg-dark-100">
              <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{{ mes }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ 8 + i }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ (1200 + i * 50).toLocaleString('pt-BR') }}</td>
              <td class="px-6 py-4 text-green-600">{{ (400 + i * 20).toLocaleString('pt-BR') }}</td>
              <td class="px-6 py-4 text-gray-600 dark:text-gray-400">{{ formatCurrency(1800 + i * 100) }}</td>
              <td class="px-6 py-4 text-green-600">-{{ formatCurrency(450 + i * 30) }}</td>
              <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white">{{ formatCurrency(1350 + i * 70) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
