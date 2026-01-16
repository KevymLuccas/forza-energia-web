<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue: string
  label?: string
  type?: string
  placeholder?: string
  error?: string
  icon?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  error: '',
  disabled: false
})

const emit = defineEmits(['update:modelValue'])

const localValue = ref(props.modelValue)
const showPassword = ref(false)

watch(() => props.modelValue, (newVal) => {
  localValue.value = newVal
})

function updateValue(event: Event) {
  const target = event.target as HTMLInputElement
  localValue.value = target.value
  emit('update:modelValue', target.value)
}

const inputType = ref(props.type)

function togglePassword() {
  if (props.type === 'password') {
    showPassword.value = !showPassword.value
    inputType.value = showPassword.value ? 'text' : 'password'
  }
}
</script>

<template>
  <div class="space-y-1.5">
    <label v-if="label" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
      {{ label }}
    </label>
    
    <div class="relative">
      <!-- Left Icon -->
      <div v-if="icon" class="absolute left-3 top-1/2 -translate-y-1/2">
        <svg v-if="icon === 'email'" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        <svg v-if="icon === 'lock'" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <svg v-if="icon === 'user'" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </div>
      
      <input 
        :type="inputType"
        :value="localValue"
        :placeholder="placeholder"
        :disabled="disabled"
        @input="updateValue"
        class="w-full py-3 rounded-xl border bg-white dark:bg-dark-100 
               text-gray-900 dark:text-white placeholder-gray-400
               focus:ring-2 focus:ring-primary-500 focus:border-transparent
               transition-all duration-300 outline-none
               disabled:opacity-50 disabled:cursor-not-allowed"
        :class="[
          icon ? 'pl-10' : 'pl-4',
          type === 'password' ? 'pr-10' : 'pr-4',
          error ? 'border-red-500 dark:border-red-500' : 'border-gray-200 dark:border-gray-700'
        ]"
      />
      
      <!-- Password Toggle -->
      <button 
        v-if="type === 'password'"
        type="button"
        @click="togglePassword"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
      >
        <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
      </button>
    </div>
    
    <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
  </div>
</template>
