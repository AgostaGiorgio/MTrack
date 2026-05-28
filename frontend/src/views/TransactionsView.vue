<script setup>
import { ref, computed } from 'vue'
import * as Icons from 'lucide-vue-next'

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
      <div v-for="tx in transactions" :key="tx.id" 
           class="bg-brand-surface p-4 rounded-app-sm shadow-sm border border-white/5 flex flex-col gap-3">
        
        <div class="flex justify-between items-start">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-brand-background flex items-center justify-center flex-shrink-0">
              <component :is="getCategoryIcon(tx.primary)" class="w-5 h-5 text-brand-primary" />
            </div>
            <div>
              <div class="text-brand-textMain font-bold text-base leading-tight">{{ tx.description }}</div>
              <div class="flex items-center gap-1 text-xs text-brand-textMuted mt-1">
                <Icons.CreditCard class="w-3 h-3" />
                <span>{{ tx.card }}</span>
                <span class="mx-1">•</span>
                <span>{{ formatDate(tx.date) }}</span>
              </div>
            </div>
          </div>
          <div class="text-brand-textMain font-extrabold">
            € {{ tx.amount.toFixed(2) }}
          </div>
        </div>

        <div class="mt-1 pt-3 border-t border-white/5">
          <button @click="openSheet(tx)" 
                  class="w-full flex items-center justify-between bg-brand-background/50 hover:bg-brand-background/80 transition-colors p-2.5 rounded-lg border border-white/5">
            <div class="flex items-center gap-2 text-sm">
              <span class="font-medium" :class="tx.primary ? 'text-brand-primary' : 'text-brand-textMuted'">
                {{ tx.primary || 'Uncategorized' }}
              </span>
              <span v-if="tx.secondary" class="text-brand-textMuted text-xs">/</span>
              <span v-if="tx.secondary" class="text-brand-textMuted text-xs font-medium">{{ tx.secondary }}</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-brand-textMuted">
              <span>Edit</span>
              <Icons.ChevronRight class="w-4 h-4" />
            </div>
          </button>
        </div>
        
      </div>
    </div>

    <Teleport to="body">
      <transition enter-active-class="transition-opacity duration-300" leave-active-class="transition-opacity duration-300" enter-from-class="opacity-0" leave-to-class="opacity-0">
        <div v-if="editingTx" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60]" @click="closeSheet"></div>
      </transition>

      <transition enter-active-class="transition-transform duration-300 cubic-bezier(0.4, 0, 0.2, 1)" leave-active-class="transition-transform duration-300 cubic-bezier(0.4, 0, 0.2, 1)" enter-from-class="translate-y-full" leave-to-class="translate-y-full">
        <div v-if="editingTx" class="fixed bottom-0 left-0 w-full bg-brand-surface rounded-t-app shadow-app border-t border-white/10 p-6 z-[70] pb-10">
          
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl font-bold text-brand-textMain">Assign Category</h3>
            <button @click="closeSheet" class="w-8 h-8 rounded-full bg-brand-background flex items-center justify-center text-brand-textMuted">
              <Icons.X class="w-5 h-5" />
            </button>
          </div>

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
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script>
import { ChevronDown } from 'lucide-vue-next'
export default { components: { ChevronDown } }
</script>