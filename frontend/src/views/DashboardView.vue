<script setup>
import { ref } from 'vue'
import CategoryChart from '../components/CategoryChart.vue'

const currentMonth = ref('May 2026')
const totalSpent = ref(1250.40)

const cardsSummary = ref([
  { name: 'Main Card', amount: 850.20 },
  { name: 'Revolut', amount: 400.20 }
])

const categorySummary = ref([
  { name: 'Groceries', amount: 450.00, color: '#8b5cf6' }, 
  { name: 'Transport', amount: 150.00, color: '#c084fc' },
  { name: 'Dining', amount: 300.00, color: '#6366f1' },
  { name: 'Utilities', amount: 350.40, color: '#3b82f6' }
])
</script>

<template>
  <div class="py-2 flex flex-col gap-8">
    
    <section class="flex flex-col items-center justify-center mt-2">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">{{ currentMonth }}</span>
      </div>
      <h2 class="text-5xl font-extrabold tracking-tighter text-brand-textMain">
        € {{ totalSpent.toFixed(2) }}
      </h2>
    </section>

    <section class="flex gap-4 overflow-x-auto pb-4 hide-scrollbar">
      <div v-for="card in cardsSummary" :key="card.name" 
           class="min-w-[140px] bg-brand-surface p-5 rounded-app shadow-sm border border-white/5 flex-shrink-0">
        <div class="text-xs text-brand-textMuted mb-2 font-medium">{{ card.name }}</div>
        <div class="text-xl font-bold text-brand-textMain">€ {{ card.amount.toFixed(2) }}</div>
      </div>
    </section>

    <section class="bg-brand-surface p-6 rounded-app shadow-sm border border-white/5 flex flex-col items-center mb-6">
      <h3 class="text-sm font-semibold text-brand-textMuted self-start mb-8">Expenses by Category</h3>
      
      <div class="mb-8 relative flex justify-center items-center">
        <CategoryChart :categories="categorySummary" />
      </div>

      <div class="w-full flex flex-col gap-3">
        <div v-for="cat in categorySummary" :key="cat.name" class="flex justify-between items-center text-sm">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full shadow-sm" :style="{ backgroundColor: cat.color }"></span>
            <span class="text-brand-textMain font-medium">{{ cat.name }}</span>
          </div>
          <span class="text-brand-textMuted">€ {{ cat.amount.toFixed(2) }}</span>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>