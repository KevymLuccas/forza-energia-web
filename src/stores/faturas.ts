import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/lib/api'

export interface Fatura {
  id: string
  vencimento: string
  diasLeitura: number
  energiaInjetada: number
  saldoUtilizado: number
  saldoAtualizado: number
  totalPagar: number
  leituraAnteriorData: string
  leituraAtualData: string
  proximaLeituraData: string
  consumoKwh: number
  leituraAtual: number
  leituraAnterior: number
  energiaAtivaTE: number
  energiaAtivaTUSD: number
  energiaInjetadaTE: number
  energiaInjetadaTUSD: number
  bandeiraAmarelaComp: number
  bandeiraVermelhaComp: number
  bandeiraAmarela: number
  bandeiraVermelha: number
  iluminacaoPublica: number
  valoresNegativos: number
  valoresPositivos: number
  unidadeConsumidora: string
  numeroCliente: string
  status: 'pendente' | 'processando' | 'concluido' | 'erro'
  createdAt: string
}

export const useFaturasStore = defineStore('faturas', () => {
  const faturas = ref<Fatura[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const processandoCount = ref(0)

  async function fetchFaturas() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/faturas')
      faturas.value = Array.isArray(response.data) ? response.data : []
    } catch (e: any) {
      error.value = e.message || 'Erro ao carregar faturas'
      faturas.value = []
    } finally {
      loading.value = false
    }
  }

  async function uploadFatura(file: File) {
    loading.value = true
    error.value = null
    processandoCount.value++
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await api.post('/extract', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      if (response.data) {
        faturas.value.unshift(response.data)
      }
      
      return { success: true, data: response.data }
    } catch (e: any) {
      error.value = e.message || 'Erro ao processar fatura'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
      processandoCount.value--
    }
  }

  async function baixarDoGmail() {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/gmail/baixar')
      return { success: true, data: response.data }
    } catch (e: any) {
      error.value = e.message || 'Erro ao baixar faturas do Gmail'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function processarTodas() {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/processar-todas')
      await fetchFaturas()
      return { success: true, data: response.data }
    } catch (e: any) {
      error.value = e.message || 'Erro ao processar faturas'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  function getStats() {
    const lista = Array.isArray(faturas.value) ? faturas.value : []
    const total = lista.length
    const pendentes = lista.filter(f => f.status === 'pendente').length
    const processando = lista.filter(f => f.status === 'processando').length
    const concluidas = lista.filter(f => f.status === 'concluido').length
    const erros = lista.filter(f => f.status === 'erro').length
    
    const valorTotal = lista
      .filter(f => f.status === 'concluido')
      .reduce((acc, f) => acc + (f.totalPagar || 0), 0)
    
    const consumoTotal = lista
      .filter(f => f.status === 'concluido')
      .reduce((acc, f) => acc + (f.consumoKwh || 0), 0)

    return { total, pendentes, processando, concluidas, erros, valorTotal, consumoTotal }
  }

  return {
    faturas,
    loading,
    error,
    processandoCount,
    fetchFaturas,
    uploadFatura,
    baixarDoGmail,
    processarTodas,
    getStats
  }
})
