<script setup>
import { ref, computed, onMounted } from 'vue'
import { ChevronDown, ChevronUp, CreditCard, Tags, BarChart3 } from 'lucide-vue-next'

import { api } from '../services/api'
import { stringToColor } from '../utils/colors'
import MoneyValue from '../components/ui/MoneyValue.vue'
import LoadingSkeleton from '../components/ui/LoadingSkeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import CategoryChart from '../components/CategoryChart.vue'
import MonthlyChart from '../components/MonthlyChart.vue'

const currentMonth = ref('')
const totalSpent = ref(0)
const cardsSummary = ref([])
const categorySummary = ref([])
const monthlyTrend = ref([])
const loading = ref(true)

const expandedCategoryId = ref(null)

const normalizedCategory = (category) => {
  const name = category.name || 'Uncategorized'
  return {
    id: category.id || name,
    name,
    amount: Number(category.amount) || 0,
    color: stringToColor(name),
    sub_categories: (category.sub_categories || []).map(normalizedCategory),
  }
}

const toggleCategory = (categoryId) => {
  expandedCategoryId.value = expandedCategoryId.value === categoryId ? null : categoryId
}

const averagePerCard = computed(() =>
  cardsSummary.value.length ? totalSpent.value / cardsSummary.value.length : 0,
)

const loadDashboardData = async () => {
  loading.value = true
  try {
    const rawDashboardData = await api.getDashboardData()

    currentMonth.value = rawDashboardData.current_month
    totalSpent.value = Number(rawDashboardData.total_spent) || 0
    cardsSummary.value = (rawDashboardData.cards_summary || []).map((card) => ({
      ...card,
      name: card.name || 'Unknown card',
      amount: Number(card.amount) || 0,
    }))
    monthlyTrend.value = rawDashboardData.monthly_trends || []
    categorySummary.value = (rawDashboardData.categories_summary || []).map(normalizedCategory)
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-5 w-full">
      <LoadingSkeleton v-if="loading" :lines="4" height="h-24" />

      <template v-else>
        <!-- Totals and cards: side by side on desktop -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Hero: current month total -->
          <section class="app-card rounded-app p-5 flex flex-col gap-4 h-full">
            <div class="flex flex-col gap-1">
              <span
                class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted"
              >
                {{ currentMonth || 'This month' }}
              </span>
              <div class="text-4xl font-extrabold tracking-tighter">
                <MoneyValue :value="totalSpent" />
              </div>
              <span class="text-xs font-medium text-brand-textMuted">total spent</span>
            </div>

            <div class="mt-auto grid grid-cols-3 gap-2 pt-4 border-t border-white/5">
              <div class="flex flex-col gap-0.5">
                <span
                  class="text-[10px] uppercase tracking-widest font-semibold text-brand-textMuted"
                  >Cards</span
                >
                <span class="text-brand-textMain text-sm font-bold">{{ cardsSummary.length }}</span>
              </div>
              <div class="flex flex-col gap-0.5">
                <span
                  class="text-[10px] uppercase tracking-widest font-semibold text-brand-textMuted"
                  >Categories</span
                >
                <span class="text-brand-textMain text-sm font-bold">{{
                  categorySummary.length
                }}</span>
              </div>
              <div class="flex flex-col gap-0.5">
                <span
                  class="text-[10px] uppercase tracking-widest font-semibold text-brand-textMuted"
                  >Avg / card</span
                >
                <MoneyValue :value="averagePerCard" class="text-brand-textMain text-sm font-bold" />
              </div>
            </div>
          </section>

          <!-- Cards -->
          <section class="app-card rounded-app p-5 flex flex-col gap-3 h-full">
            <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">
              Cards
            </h2>

            <div v-if="cardsSummary.length" class="flex flex-col divide-y divide-white/5">
              <div
                v-for="card in cardsSummary"
                :key="card.name"
                class="flex items-center gap-3 py-3 first:pt-0 last:pb-0"
              >
                <span
                  class="w-8 h-8 rounded-full bg-brand-background border border-white/5 flex items-center justify-center shrink-0"
                >
                  <CreditCard :size="15" class="text-brand-primary" />
                </span>
                <span class="flex-1 min-w-0 text-brand-textMain text-sm font-medium truncate">{{
                  card.name
                }}</span>
                <MoneyValue :value="card.amount" class="text-brand-textMain text-sm font-bold" />
              </div>
            </div>

            <EmptyState
              v-else
              :icon="CreditCard"
              title="No card activity"
              description="No expenses recorded for this month."
            />
          </section>
        </div>

        <!-- Expenses by category -->
        <section class="app-card rounded-app p-5 flex flex-col gap-4">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">
            By category
          </h2>

          <template v-if="categorySummary.length">
            <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:gap-8">
              <div class="flex justify-center py-1 lg:w-2/5 lg:shrink-0">
                <CategoryChart :categories="categorySummary" class="lg:w-64 lg:h-64" />
              </div>

              <div class="flex flex-col divide-y divide-white/5 lg:flex-1">
                <div v-for="cat in categorySummary" :key="cat.id">
                  <button
                    type="button"
                    :disabled="cat.sub_categories.length === 0"
                    @click="toggleCategory(cat.id)"
                    class="w-full flex justify-between items-center gap-3 py-3 text-left disabled:cursor-default"
                  >
                    <span class="flex items-center gap-2 min-w-0">
                      <span
                        class="w-2.5 h-2.5 rounded-full shrink-0"
                        :style="{ backgroundColor: cat.color }"
                      />
                      <span class="text-brand-textMain text-sm font-medium truncate">{{
                        cat.name
                      }}</span>
                    </span>

                    <span class="flex items-center gap-2 shrink-0">
                      <MoneyValue
                        :value="cat.amount"
                        class="text-brand-textMuted text-xs font-semibold"
                      />
                      <component
                        v-if="cat.sub_categories.length"
                        :is="expandedCategoryId === cat.id ? ChevronUp : ChevronDown"
                        :size="14"
                        class="text-brand-textMuted transition-transform"
                      />
                      <span v-else class="w-3.5" />
                    </span>
                  </button>

                  <div
                    v-if="cat.sub_categories.length"
                    class="grid transition-[grid-template-rows,opacity] duration-300 ease-in-out"
                    :class="
                      expandedCategoryId === cat.id
                        ? 'grid-rows-[1fr] opacity-100'
                        : 'grid-rows-[0fr] opacity-0'
                    "
                  >
                    <div class="overflow-hidden">
                      <div class="flex flex-col gap-2 pb-3 pl-[18px] ml-1 border-l border-white/10">
                        <div
                          v-for="sub in cat.sub_categories"
                          :key="sub.id"
                          class="flex justify-between items-center gap-3 text-xs"
                        >
                          <span class="text-brand-textMuted truncate">{{ sub.name }}</span>
                          <MoneyValue :value="sub.amount" class="text-brand-textMuted shrink-0" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <EmptyState
            v-else
            :icon="Tags"
            title="No categories yet"
            description="Categories will show up once expenses are recorded."
          />
        </section>

        <!-- Monthly trend -->
        <section class="app-card rounded-app p-5 flex flex-col gap-3">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">
            Months trend
          </h2>

          <MonthlyChart v-if="monthlyTrend.length" :data="monthlyTrend" />

          <EmptyState
            v-else
            :icon="BarChart3"
            title="No trend data"
            description="Monthly totals will appear here."
          />
        </section>
      </template>
    </div>
  </main>
</template>
