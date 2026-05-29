<script setup>
import { ref, computed, onMounted } from 'vue'

import { api } from '../services/api'
import { ChevronDown, ChevronUp } from 'lucide-vue-next'
import CategoryChart from '../components/CategoryChart.vue'
import MonthlyChart from '../components/MonthlyChart.vue'

const currentMonth = ref('')
const totalSpent = ref(0)
const cardsSummary = ref([])
const categorySummary = ref([])
const monthlyTrend = ref([])

const expandedCategory = ref(null)

const stringToColor = (str) => {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const h = Math.abs(hash) % 360
  return `hsl(${h}, 70%, 65%)`
}

const toggleCategory = (categoryName) => {
  if (expandedCategory.value === categoryName) {
    expandedCategory.value = null
  } else {
    expandedCategory.value = categoryName
  }
}

const loadDashboardData = async () => {
  try {
    const [rawDashboardData] = await Promise.all([
      api.getDashboardData()
    ])

    currentMonth.value = rawDashboardData.current_month
    totalSpent.value = rawDashboardData.total_spent
    cardsSummary.value = rawDashboardData.cards_summary
    monthlyTrend.value = rawDashboardData.monthly_trends

    const categorySummaryWithColor = computed(() => {
      return rawDashboardData.categories_summary.map(cat => ({
        ...cat,
        color: stringToColor(cat.name)
      }))
    })
    categorySummary.value = categorySummaryWithColor.value
  } catch (error) {
    console.error("Errore fatale nel caricamento del carosello:", error)
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<template>
  <div class="py-2 flex flex-col gap-7">
    
    <section class="flex flex-col items-center justify-center">
      <div class="flex items-center gap-2">
        <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">{{ currentMonth }}</span>
      </div>
      <h2 class="text-5xl font-extrabold tracking-tighter text-brand-textMain">
        Đ {{ totalSpent.toFixed(2) }}
      </h2>
    </section>

    <section class="flex gap-4 overflow-x-auto hide-scrollbar">
      <div v-for="card in cardsSummary" :key="card.name" 
           class="min-w-[140px] bg-brand-surface p-4 rounded-app shadow-sm border border-white/5 flex-shrink-0">
        <div class="text-xs text-brand-textMuted font-medium">{{ card.name }}</div>
        <div class="text-xl font-bold text-brand-textMain">Đ {{ card.amount.toFixed(2) }}</div>
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
            @click="cat.sub_categories.length > 0 ? toggleCategory(cat.name) : null"
            class="flex justify-between items-center text-sm py-1"
            :class="{ 'cursor-pointer': cat.sub_categories.length > 0 }"
          >
            <div class="flex items-center gap-3">
              <span class="w-3 h-3 rounded-full shadow-sm flex-shrink-0" :style="{ backgroundColor: cat.color }"></span>
              <span class="text-brand-textMain font-medium">{{ cat.name }}</span>
            </div>
            
            <div class="flex items-center gap-2">
              <span class="text-brand-textMuted">Đ {{ cat.amount.toFixed(2) }}</span>
              <component 
                v-if="cat.sub_categories.length > 0"
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
                <div v-for="sub in cat.sub_categories" :key="sub.name" class="flex justify-between items-center text-xs">
                  <span class="text-brand-textMuted">{{ sub.name }}</span>
                  <span class="text-brand-textMuted">Đ {{ sub.amount.toFixed(2) }}</span>
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