<script setup>
import { ref, computed } from 'vue'
import * as Icons from 'lucide-vue-next'
import TransactionItem from '../components/TransactionItem.vue'
import BottomSheet from '../components/BottomSheet.vue'

const transactions = ref([
  { id: 1, date: '2026-05-28T10:30:00Z', description: 'Amazon AWS', amount: 45.00, card: 'Main Card', primary: 'Utilities', secondary: 'Internet' },
  { id: 2, date: '2026-05-27T18:15:00Z', description: 'Shell Station', amount: 60.50, card: 'Revolut', primary: 'Car', secondary: 'Fuel' },
  { id: 3, date: '2026-05-26T20:00:00Z', description: 'Sushi Bar', amount: 85.00, card: 'Main Card', primary: 'Dining', secondary: null },
  { id: 4, date: '2026-05-25T09:00:00Z', description: 'Supermarket', amount: 120.30, card: 'Revolut', primary: 'Groceries', secondary: null },
])

const categoriesDB = ref([
  { name: 'Car', icon: 'Car', subs: ['Fuel', 'Parking', 'Maintenance'] },
  { name: 'Utilities', icon: 'Zap', subs: ['Internet', 'Electricity', 'Water'] },
  { name: 'Dining', icon: 'UtensilsCrossed', subs: [] },
  { name: 'Groceries', icon: null, subs: [] },
])

const getCategoryIcon = (categoryName) => {
  if (!categoryName) return Icons.undefined

  const cat = categoriesDB.value.find(c => c.name === categoryName)
  const iconName = cat && cat.icon ? cat.icon : 'CircleDollarSign'
  
  return Icons[iconName] || Icons.undefined
}

const editingTx = ref(null)

const openSheet = (tx) => {
  editingTx.value = { ...tx } 
}

const closeSheet = () => {
  editingTx.value = null
}

const saveCategories = () => {
  const index = transactions.value.findIndex(t => t.id === editingTx.value.id)
  if (index !== -1) {
    transactions.value[index] = { ...editingTx.value }
  }
  closeSheet()
}

const handlePrimaryChange = () => {
  editingTx.value.secondary = null
}

const availableSubs = computed(() => {
  if (!editingTx.value || !editingTx.value.primary) return []
  const cat = categoriesDB.value.find(c => c.name === editingTx.value.primary)
  return cat ? cat.subs : []
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
}
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
        :iconComponent="getCategoryIcon(tx.primary)"
        @edit="openSheet"
      />
    </div>

    <BottomSheet :isOpen="!!editingTx" title="Assign Category" @close="closeSheet">
      <div class="flex justify-between items-center mb-8 p-3 bg-brand-background rounded-lg border border-white/5">
        <span class="text-brand-textMuted text-sm truncate pr-2">{{ editingTx.description }}</span>
        <span class="text-brand-textMain font-bold">€ {{ editingTx.amount.toFixed(2) }}</span>
      </div>

      <div class="flex flex-col gap-5">
        
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Primary Category</label>
          <div class="relative">
            <select v-model="editingTx.primary" @change="handlePrimaryChange" 
                    class="w-full appearance-none bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-4 pr-10 focus:outline-none focus:border-brand-primary font-medium">
              <option disabled :value="null">Select category...</option>
              <option v-for="cat in categoriesDB" :key="cat.name" :value="cat.name">
                {{ cat.name }}
              </option>
            </select>
            <Icons.ChevronDown class="w-5 h-5 absolute right-4 top-4 text-brand-textMuted pointer-events-none" />
          </div>
        </div>

        <div class="flex flex-col gap-2" v-if="availableSubs.length > 0">
          <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Secondary Category</label>
          <div class="relative">
            <select v-model="editingTx.secondary" 
                    class="w-full appearance-none bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-4 pr-10 focus:outline-none focus:border-brand-primary font-medium">
              <option :value="null">None</option>
              <option v-for="sub in availableSubs" :key="sub" :value="sub">
                {{ sub }}
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