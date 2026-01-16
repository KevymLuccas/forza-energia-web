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

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errors = ref({ name: '', email: '', password: '', confirmPassword: '' })

async function handleRegister() {
  errors.value = { name: '', email: '', password: '', confirmPassword: '' }
  
  if (!name.value) {
    errors.value.name = 'Nome é obrigatório'
    return
  }
  if (!email.value) {
    errors.value.email = 'Email é obrigatório'
    return
  }
  if (!password.value) {
    errors.value.password = 'Senha é obrigatória'
    return
  }
  if (password.value.length < 6) {
    errors.value.password = 'Senha deve ter no mínimo 6 caracteres'
    return
  }
  if (password.value !== confirmPassword.value) {
    errors.value.confirmPassword = 'As senhas não conferem'
    return
  }
  
  loading.value = true
  const result = await authStore.register(email.value, password.value, name.value)
  loading.value = false
  
  if (result.success) {
    toast.success('Conta criada com sucesso! Verifique seu email.')
    router.push('/login')
  } else {
    toast.error(result.error || 'Erro ao criar conta')
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
    <!-- Left Side - Form -->
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
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Criar conta</h2>
          <p class="mt-2 text-gray-600 dark:text-gray-400">Preencha os dados para criar sua conta</p>
        </div>
        
        <!-- Form -->
        <form @submit.prevent="handleRegister" class="space-y-5">
          <Input 
            v-model="name"
            type="text"
            label="Nome completo"
            placeholder="Seu nome"
            icon="user"
            :error="errors.name"
          />
          
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
          
          <Input 
            v-model="confirmPassword"
            type="password"
            label="Confirmar senha"
            placeholder="••••••••"
            icon="lock"
            :error="errors.confirmPassword"
          />
          
          <label class="flex items-start gap-2 cursor-pointer">
            <input type="checkbox" class="w-4 h-4 mt-0.5 rounded border-gray-300 text-primary-500 focus:ring-primary-500" required />
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Concordo com os 
              <a href="#" class="text-primary-600 hover:text-primary-500">Termos de Uso</a> 
              e 
              <a href="#" class="text-primary-600 hover:text-primary-500">Política de Privacidade</a>
            </span>
          </label>
          
          <Button type="submit" :loading="loading" block>
            Criar conta
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
        
        <!-- Login Link -->
        <p class="text-center text-sm text-gray-600 dark:text-gray-400">
          Já tem uma conta? 
          <router-link to="/login" class="text-primary-600 hover:text-primary-500 font-medium">
            Faça login
          </router-link>
        </p>
      </div>
    </div>
    
    <!-- Right Side - Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 to-primary-800 p-12 flex-col justify-between relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-10">
        <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <defs>
            <pattern id="grid2" width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" fill="none" stroke="white" stroke-width="0.5"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#grid2)" />
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
          Comece a automatizar<br />suas faturas hoje
        </h1>
        <p class="text-lg text-white/80 max-w-md">
          Junte-se a centenas de empresas que já otimizaram seu processo de gestão de faturas de energia.
        </p>
        
        <!-- Features -->
        <div class="space-y-4 pt-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span class="text-white/90">Extração automática com IA</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span class="text-white/90">Integração com Gmail e Drive</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span class="text-white/90">Relatórios detalhados</span>
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="relative z-10 text-white/60 text-sm">
        © 2026 Forza Energia. Todos os direitos reservados.
      </div>
    </div>
  </div>
</template>
