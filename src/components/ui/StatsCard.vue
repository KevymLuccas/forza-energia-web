<script setup lang="ts">
interface Props {
  title: string
  value: string | number
  icon: string
  trend?: number
  trendLabel?: string
  color?: 'green' | 'blue' | 'yellow' | 'red' | 'purple'
}

const props = withDefaults(defineProps<Props>(), {
  color: 'green',
  trend: 0,
  trendLabel: ''
})

const colorClasses = {
  green: 'from-green-500 to-emerald-600',
  blue: 'from-blue-500 to-indigo-600',
  yellow: 'from-yellow-500 to-orange-500',
  red: 'from-red-500 to-rose-600',
  purple: 'from-purple-500 to-violet-600'
}

const bgClasses = {
  green: 'bg-green-500/10',
  blue: 'bg-blue-500/10',
  yellow: 'bg-yellow-500/10',
  red: 'bg-red-500/10',
  purple: 'bg-purple-500/10'
}
</script>

<template>
  <div class="bg-white dark:bg-dark-200 rounded-2xl p-6 card-hover border border-gray-100 dark:border-gray-800">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{{ title }}</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ value }}</p>
        
        <div v-if="trend !== 0" class="flex items-center gap-1 mt-2">
          <svg 
            class="w-4 h-4" 
            :class="trend > 0 ? 'text-green-500' : 'text-red-500'"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path 
              stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              :d="trend > 0 ? 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' : 'M13 17h8m0 0V9m0 8l-8-8-4 4-6-6'" 
            />
          </svg>
          <span 
            class="text-sm font-medium"
            :class="trend > 0 ? 'text-green-500' : 'text-red-500'"
          >
            {{ Math.abs(trend) }}%
          </span>
          <span class="text-xs text-gray-500 dark:text-gray-400">{{ trendLabel }}</span>
        </div>
      </div>
      
      <div 
        class="w-14 h-14 rounded-2xl flex items-center justify-center"
        :class="bgClasses[color]"
      >
        <!-- Bolt Icon -->
        <svg v-if="icon === 'bolt'" class="w-7 h-7" :class="`bg-gradient-to-r ${colorClasses[color]} bg-clip-text`" style="color: transparent; background-clip: text; -webkit-background-clip: text;" fill="currentColor" viewBox="0 0 24 24">
          <path d="M13 10V3L4 14h7v7l9-11h-7z" fill="url(#grad)" />
          <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" :style="`stop-color: var(--tw-gradient-from)`" />
              <stop offset="100%" :style="`stop-color: var(--tw-gradient-to)`" />
            </linearGradient>
          </defs>
        </svg>
        
        <!-- Money Icon -->
        <svg v-if="icon === 'money'" class="w-7 h-7 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        
        <!-- Document Icon -->
        <svg v-if="icon === 'document'" class="w-7 h-7 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        
        <!-- Users Icon -->
        <svg v-if="icon === 'users'" class="w-7 h-7 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        
        <!-- Check Icon -->
        <svg v-if="icon === 'check'" class="w-7 h-7 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        
        <!-- Clock Icon -->
        <svg v-if="icon === 'clock'" class="w-7 h-7 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
    </div>
  </div>
</template>
