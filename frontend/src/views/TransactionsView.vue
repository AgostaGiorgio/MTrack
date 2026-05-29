<script setup>
import { ref, computed, onMounted } from 'vue'

import { api } from '../services/api'
import * as Icons from 'lucide-vue-next'
import TransactionItem from '../components/TransactionItem.vue'
import BottomSheet from '../components/BottomSheet.vue'

const transactions = ref([])
const categories = ref([])

const editingTx = ref(null)
const editingTxPrimaryId = ref(null)
const editingTxSecondaryId = ref(null)

const availableSubs = computed(() => {
  if (!editingTx.value || !editingTxPrimaryId.value) return []
  const cat = categories.value.find(c => c.id === editingTxPrimaryId.value)
  return cat ? cat.sub_categories : []
})

const getCategoryIcon = (category) => {
  if (!category) return Icons.Circle

  const cat = categories.value.find(c => c.id === category.id)
  const iconName = cat && cat.icon ? cat.icon : 'Circle'
  
  return Icons[iconName] || Icons.undefined
}

const openSheet = (tx) => {
  editingTx.value = { ...tx }
  editingTxPrimaryId.value = tx.primary_category ? tx.primary_category.id : null
  editingTxSecondaryId.value = tx.secondary_category ? tx.secondary_category.id : null
}

const closeSheet = () => {
  editingTx.value = null
  editingTxPrimaryId.value = null
  editingTxSecondaryId.value = null
}

const saveCategories = async () => {
  const pcat = categories.value.find(c => c.id === editingTxPrimaryId.value)
  const scat = editingTxSecondaryId.value ? pcat?.sub_categories.find(c => c.id === editingTxSecondaryId.value) : null

  editingTx.value.primary_category = pcat || null
  editingTx.value.secondary_category = scat || null

  try{
    await api.updateTransactionCategories(editingTx.value.id, editingTx.value.primary_category.id, editingTx.value.secondary_category?.id)
    await loadTransactionsData()
  } catch(error){
    console.error("Errore fatale nell'aggiornamento delle categorie della transazione:", error)
  } finally { 
    closeSheet()
  }
}

const handlePrimaryChange = () => {
  editingTx.value.secondary_category = null
}

const loadTransactionsData = async () => {
  try {
    const [rawTransactionsData, rawCategoriesData] = await Promise.all([
      api.getTransactions(),
      api.getCategories()
    ])

    transactions.value = rawTransactionsData
    categories.value = rawCategoriesData
  } catch (error) {
    console.error("Errore fatale nel caricamento delle transazioni o delle categorie:", error)
  }
}

onMounted(() => {
  loadTransactionsData()
})
</script>

<template>
  <div class="py-4 flex flex-col h-full">
    
    <header class="mb-6 mt-2 flex justify-between items-end">
      <div>
        <h2 class="text-3xl font-extrabold tracking-tighter text-brand-textMain">Transactions</h2>
        <p class="text-sm text-brand-textMuted mt-1">May 2026 • {{ transactions.length }} operations</p>
      </div>
    </header>

    <div class="flex flex-col gap-3 pb-24">
      <TransactionItem 
        v-for="tx in transactions" 
        :key="tx.id" 
        :transaction="tx"
        :iconComponent="getCategoryIcon(tx.primary_category)"
        @edit="openSheet"
      />
    </div>

    <BottomSheet :isOpen="!!editingTx" title="Assign Category" @close="closeSheet">
      <div class="flex justify-between items-center mb-8 p-3 bg-brand-background rounded-lg border border-white/5">
        <span class="text-brand-textMuted text-sm truncate pr-2">{{ editingTx.description }}</span>
        <span class="text-brand-textMain font-bold">Đ {{ editingTx.amount.toFixed(2) }}</span>
      </div>

      <div class="flex flex-col gap-5">
        
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Primary Category</label>
          <div class="relative">
            <select v-model="editingTxPrimaryId" @change="handlePrimaryChange" 
                    class="w-full appearance-none bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-4 pr-10 focus:outline-none focus:border-brand-primary font-medium">
              <option disabled :value="null">Select category...</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
            <Icons.ChevronDown class="w-5 h-5 absolute right-4 top-4 text-brand-textMuted pointer-events-none" />
          </div>
        </div>

        <div class="flex flex-col gap-2" v-if="availableSubs.length > 0">
          <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Secondary Category</label>
          <div class="relative">
            <select v-model="editingTxSecondaryId" 
                    class="w-full appearance-none bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-4 pr-10 focus:outline-none focus:border-brand-primary font-medium">
              <option :value="null">None</option>
              <option v-for="sub in availableSubs" :key="sub.id" :value="sub.id">
                {{ sub.name }}
              </option>
            </select>
            <Icons.ChevronDown class="w-5 h-5 absolute right-4 top-4 text-brand-textMuted pointer-events-none" />
          </div>
        </div>

        <button @click="saveCategories" class="mt-4 w-full bg-brand-primary text-white font-bold py-4 rounded-xl shadow-lg hover:bg-brand-secondary transition-colors">
          Save Changes
        </button>
        
      </div>
    </BottomSheet>
  </div>
</template>

<script>
import { ChevronDown } from 'lucide-vue-next'
export default { components: { ChevronDown } }
</script>