<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errors = ref({ email: '', password: '' })

async function handleLogin() {
  errors.value = { email: '', password: '' }
  
  if (!email.value) {
    errors.value.email = 'Email é obrigatório'
    return
  }
  if (!password.value) {
    errors.value.password = 'Senha é obrigatória'
    return
  }
  
  loading.value = true
  const result = await authStore.login(email.value, password.value)
  loading.value = false
  
  if (result.success) {
    toast.success('Login realizado com sucesso!')
    router.push('/')
  } else {
    toast.error(result.error || 'Erro ao fazer login')
  }
}

async function handleGoogleLogin() {
  loading.value = true
  const result = await authStore.loginWithGoogle()
  loading.value = false
  
  if (!result.success) {
    toast.error(result.error || 'Erro ao fazer login com Google')
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-dark-300 dark:to-dark-200 flex">
    <!-- Left Side - Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-500 to-primary-700 p-12 flex-col justify-between relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-10">
        <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <defs>
            <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" fill="none" stroke="white" stroke-width="0.5"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#grid)" />
        </svg>
      </div>
      
      <!-- Logo -->
      <div class="relative z-10">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span class="text-2xl font-bold text-white">Forza Energia</span>
        </div>
      </div>
      
      <!-- Content -->
      <div class="relative z-10 space-y-6">
        <h1 class="text-4xl lg:text-5xl font-bold text-white leading-tight">
          Gestão inteligente<br />de faturas de energia
        </h1>
        <p class="text-lg text-white/80 max-w-md">
          Automatize a extração de dados das suas faturas com inteligência artificial e organize tudo em um só lugar.
        </p>
        
        <div class="flex items-center gap-6 pt-4">
          <div class="text-center">
            <p class="text-3xl font-bold text-white">+500</p>
            <p class="text-sm text-white/70">Faturas processadas</p>
          </div>
          <div class="w-px h-12 bg-white/30"></div>
          <div class="text-center">
            <p class="text-3xl font-bold text-white">99%</p>
            <p class="text-sm text-white/70">Precisão IA</p>
          </div>
          <div class="w-px h-12 bg-white/30"></div>
          <div class="text-center">
            <p class="text-3xl font-bold text-white">24/7</p>
            <p class="text-sm text-white/70">Disponibilidade</p>
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="relative z-10 text-white/60 text-sm">
        © 2026 Forza Energia. Todos os direitos reservados.
      </div>
    </div>
    
    <!-- Right Side - Form -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-md space-y-8">
        <!-- Mobile Logo -->
        <div class="lg:hidden text-center">
          <div class="inline-flex items-center gap-3 mb-8">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span class="text-2xl font-bold gradient-text">Forza Energia</span>
          </div>
        </div>
        
        <!-- Header -->
        <div class="text-center lg:text-left">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Bem-vindo de volta</h2>
          <p class="mt-2 text-gray-600 dark:text-gray-400">Entre com suas credenciais para acessar o sistema</p>
        </div>
        
        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <Input 
            v-model="email"
            type="email"
            label="Email"
            placeholder="seu@email.com"
            icon="email"
            :error="errors.email"
          />
          
          <Input 
            v-model="password"
            type="password"
            label="Senha"
            placeholder="••••••••"
            icon="lock"
            :error="errors.password"
          />
          
          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="w-4 h-4 rounded border-gray-300 text-primary-500 focus:ring-primary-500" />
              <span class="text-sm text-gray-600 dark:text-gray-400">Lembrar-me</span>
            </label>
            <a href="#" class="text-sm text-primary-600 hover:text-primary-500 font-medium">Esqueceu a senha?</a>
          </div>
          
          <Button type="submit" :loading="loading" block>
            Entrar
          </Button>
        </form>
        
        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200 dark:border-gray-700"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-gray-50 dark:bg-dark-300 text-gray-500">ou continue com</span>
          </div>
        </div>
        
        <!-- Social Login -->
        <Button variant="secondary" block @click="handleGoogleLogin" :loading="loading">
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          <span>Google</span>
        </Button>
        
        <!-- Register Link -->
        <p class="text-center text-sm text-gray-600 dark:text-gray-400">
          Não tem uma conta? 
          <router-link to="/register" class="text-primary-600 hover:text-primary-500 font-medium">
            Cadastre-se
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>
