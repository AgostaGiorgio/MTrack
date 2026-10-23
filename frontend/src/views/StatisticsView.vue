<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'
import { BarChart3 } from 'lucide-vue-next'

import { api } from '../services/api'
import { stringToColor } from '../utils/colors'
import { formatMoney } from '../utils/format'
import MonthlyChart from '../components/MonthlyChart.vue'
import MoneyValue from '../components/ui/MoneyValue.vue'
import LoadingSkeleton from '../components/ui/LoadingSkeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip)

// Categories tracked on the statistics page.
const TRACKED_CATEGORIES = ['Bills', 'Food']

const stats = ref(null)
const loading = ref(true)

const previousMonths = computed(() => {
  if (!stats.value?.monthly_trends?.length) return []
  return stats.value.monthly_trends.slice(0, -1)
})

const averageMonthly = computed(() => {
  const prev = previousMonths.value
  if (!prev.length) return 0
  return prev.reduce((sum, m) => sum + m.amount, 0) / prev.length
})

const vsAveragePercent = computed(() => {
  if (!averageMonthly.value || !stats.value?.total_spent) return 0
  return ((stats.value.total_spent - averageMonthly.value) / averageMonthly.value) * 100
})

const vsAverageLabel = computed(() => {
  const p = vsAveragePercent.value
  if (p > 0) return `+${p.toFixed(1)}% above average`
  if (p < 0) return `${p.toFixed(1)}% below average`
  return 'on par with average'
})

const vsAverageClass = computed(() =>
  vsAveragePercent.value > 0 ? 'text-red-400' : 'text-emerald-400'
)

const latestAmount = (catTrend) => {
  const data = catTrend.monthly_data || []
  return data.length ? data[data.length - 1].amount : 0
}

const categoryChartData = (catTrend) => ({
  labels: (catTrend.monthly_data || []).map((d) => d.month),
  datasets: [
    {
      data: (catTrend.monthly_data || []).map((d) => d.amount),
      backgroundColor: stringToColor(catTrend.category_name),
      borderRadius: 4,
      maxBarThickness: 24,
    },
  ],
})

const miniChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      titleColor: '#94a3b8',
      bodyColor: '#f8fafc',
      padding: 10,
      cornerRadius: 12,
      displayColors: false,
      callbacks: {
        label: (ctx) => ` ${formatMoney(ctx.raw)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      border: { display: false },
      ticks: { color: '#94a3b8', font: { size: 9 }, maxRotation: 0 },
    },
    y: {
      grid: { color: 'rgba(255, 255, 255, 0.05)' },
      border: { display: false },
      ticks: { display: false },
    },
  },
}

const loadStats = async () => {
  loading.value = true
  try {
    stats.value = await api.getStatistics(TRACKED_CATEGORIES)
  } catch (error) {
    console.error('Error loading statistics:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadStats)
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-5 w-full">
      <LoadingSkeleton v-if="loading" :lines="4" height="h-24" />

      <EmptyState
        v-else-if="!stats"
        :icon="BarChart3"
        title="Unable to load statistics"
        description="Please try again later."
      />

      <template v-else>
        <!-- Current month vs average -->
        <section class="app-card rounded-app p-5 flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <span class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">
              {{ stats.current_month }}
            </span>
            <div class="text-4xl font-extrabold tracking-tighter">
              <MoneyValue :value="stats.total_spent" />
            </div>
            <span class="text-xs font-semibold" :class="vsAverageClass" title="vs monthly average">
              {{ vsAverageLabel }}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-2 pt-4 border-t border-white/5">
            <div class="flex flex-col gap-0.5">
              <span class="text-[10px] uppercase tracking-widest font-semibold text-brand-textMuted">Monthly average</span>
              <MoneyValue :value="averageMonthly" class="text-brand-textMain text-sm font-bold" />
            </div>
            <div class="flex flex-col gap-0.5">
              <span class="text-[10px] uppercase tracking-widest font-semibold text-brand-textMuted">Months tracked</span>
              <span class="text-brand-textMain text-sm font-bold">{{ previousMonths.length }}</span>
            </div>
          </div>
        </section>

        <!-- Yearly trend -->
        <section class="app-card rounded-app p-5 flex flex-col gap-3">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Yearly trend</h2>

          <MonthlyChart v-if="stats.monthly_trends.length" :data="stats.monthly_trends" />

          <EmptyState v-else :icon="BarChart3" title="No trend data" description="Monthly totals will appear here." />
        </section>

        <!-- Per-category trends -->
        <template v-if="stats.category_trends.length">
          <section
            v-for="ct in stats.category_trends"
            :key="ct.category_name"
            class="app-card rounded-app p-5 flex flex-col gap-3"
          >
            <div class="flex items-center justify-between gap-3">
              <div class="flex items-center gap-2 min-w-0">
                <span
                  class="w-2.5 h-2.5 rounded-full shrink-0"
                  :style="{ backgroundColor: stringToColor(ct.category_name) }"
                />
                <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted truncate">
                  {{ ct.category_name }}
                </h2>
              </div>
              <MoneyValue :value="latestAmount(ct)" class="text-brand-textMain text-sm font-bold shrink-0" />
            </div>

            <div class="relative h-32">
              <Bar :data="categoryChartData(ct)" :options="miniChartOptions" />
            </div>
          </section>
        </template>

        <section v-else class="app-card rounded-app p-5">
          <EmptyState
            :icon="BarChart3"
            title="No category trends"
            :description="`No data for ${TRACKED_CATEGORIES.join(', ')} yet.`"
          />
        </section>
      </template>
    </div>
  </main>
</template>
