<script setup>
import { ref, computed } from 'vue'
import CategoryChart from '../components/CategoryChart.vue'
import MonthlyChart from '../components/MonthlyChart.vue'
import { ChevronDown, ChevronUp } from 'lucide-vue-next'

const currentMonth = ref('May 2026')
const totalSpent = ref(1250.40)

const cardsSummary = ref([
  { name: 'Main Card', amount: 850.20 },
  { name: 'Revolut', amount: 400.20 }
])

const stringToColor = (str) => {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const h = Math.abs(hash) % 360
  return `hsl(${h}, 70%, 65%)`
}

const rawCategories = ref([
  { 
    name: 'Car', 
    amount: 450.00,
    subcategories: [
      { name: 'Fuel', amount: 300.00 },
      { name: 'Parking', amount: 150.00 }
    ]
  }, 
  { 
    name: 'Transport', 
    amount: 150.00,
    subcategories: [
      { name: 'Train Tickets', amount: 100.00 },
      { name: 'Taxi', amount: 50.00 }
    ]
  },
  { 
    name: 'Dining', 
    amount: 300.00,
    subcategories: []
  },
  { 
    name: 'Utilities', 
    amount: 350.40,
    subcategories: [
      { name: 'Internet', amount: 40.00 },
      { name: 'Electricity', amount: 310.40 }
    ]
  }
])

const categorySummary = computed(() => {
  return rawCategories.value.map(cat => ({
    ...cat,
    color: stringToColor(cat.name)
  }))
})

const expandedCategory = ref(null)

const toggleCategory = (categoryName) => {
  if (expandedCategory.value === categoryName) {
    expandedCategory.value = null
  } else {
    expandedCategory.value = categoryName
  }
}

const monthlyTrend = ref([
  { month: 'Jan', amount: 1100.50 },
  { month: 'Feb', amount: 950.20 },
  { month: 'Mar', amount: 1300.00 },
  { month: 'Apr', amount: 1150.80 },
  { month: 'May', amount: 1250.40 },
  { month: 'Jun', amount: 0 },
  { month: 'Jul', amount: 0 },
  { month: 'Aug', amount: 0 },
  { month: 'Sep', amount: 0 },
  { month: 'Oct', amount: 0 },
  { month: 'Nov', amount: 0 },
  { month: 'Dec', amount: 0 }
])
</script>

<template>
  <div class="py-2 flex flex-col gap-7">
    
    <section class="flex flex-col items-center justify-center">
      <div class="flex items-center gap-2">
        <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">{{ currentMonth }}</span>
      </div>
      <h2 class="text-5xl font-extrabold tracking-tighter text-brand-textMain">
        € {{ totalSpent.toFixed(2) }}
      </h2>
    </section>

    <section class="flex gap-4 overflow-x-auto hide-scrollbar">
      <div v-for="card in cardsSummary" :key="card.name" 
           class="min-w-[140px] bg-brand-surface p-4 rounded-app shadow-sm border border-white/5 flex-shrink-0">
        <div class="text-xs text-brand-textMuted font-medium">{{ card.name }}</div>
        <div class="text-xl font-bold text-brand-textMain">€ {{ card.amount.toFixed(2) }}</div>
      </div>
    </section>

    <section class="bg-brand-surface p-4 rounded-app shadow-sm border border-white/5 flex flex-col items-center">
      <h3 class="text-sm font-semibold text-brand-textMuted self-start mb-8">Expenses by Category</h3>
      
      <div class="mb-8 relative flex justify-center items-center">
        <CategoryChart :categories="categorySummary" />
      </div>

      <div class="w-full flex flex-col gap-4 mt-2">
        <div v-for="cat in categorySummary" :key="cat.name" class="flex flex-col">
          
          <div 
            @click="cat.subcategories.length > 0 ? toggleCategory(cat.name) : null"
            class="flex justify-between items-center text-sm py-1"
            :class="{ 'cursor-pointer': cat.subcategories.length > 0 }"
          >
            <div class="flex items-center gap-3">
              <span class="w-3 h-3 rounded-full shadow-sm flex-shrink-0" :style="{ backgroundColor: cat.color }"></span>
              <span class="text-brand-textMain font-medium">{{ cat.name }}</span>
            </div>
            
            <div class="flex items-center gap-2">
              <span class="text-brand-textMuted">€ {{ cat.amount.toFixed(2) }}</span>
              <component 
                v-if="cat.subcategories.length > 0"
                :is="expandedCategory === cat.name ? ChevronUp : ChevronDown" 
                class="w-4 h-4 text-brand-textMuted transition-transform" 
              />
              <div v-else class="w-4 h-4"></div> 
            </div>
          </div>

          <transition 
            enter-active-class="transition-all duration-200 ease-out"
            leave-active-class="transition-all duration-150 ease-in"
            enter-from-class="opacity-0 -translate-y-2 max-h-0"
            enter-to-class="opacity-100 translate-y-0 max-h-40"
            leave-from-class="opacity-100 translate-y-0 max-h-40"
            leave-to-class="opacity-0 -translate-y-2 max-h-0"
          >
            <div v-if="expandedCategory === cat.name" class="overflow-hidden">
              <div class="pl-6 ml-1.5 mt-2 flex flex-col gap-3 border-l border-white/10 pb-2">
                <div v-for="sub in cat.subcategories" :key="sub.name" class="flex justify-between items-center text-xs">
                  <span class="text-brand-textMuted">{{ sub.name }}</span>
                  <span class="text-brand-textMuted">€ {{ sub.amount.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </section>

    <section class="bg-brand-surface p-4 rounded-app shadow-sm border border-white/5 flex flex-col">
      <h3 class="text-sm font-semibold text-brand-textMuted">Months Trend</h3>
      <MonthlyChart :data="monthlyTrend" />
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