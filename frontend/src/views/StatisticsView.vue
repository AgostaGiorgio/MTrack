<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'
import MonthlyChart from '../components/MonthlyChart.vue'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip)

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
  return ((stats.value.total_spent - averageMonthly.value) / averageMonthly.value * 100)
})

const vsAverageLabel = computed(() => {
  const p = vsAveragePercent.value
  if (p > 0) return `+${p.toFixed(1)}% above average`
  if (p < 0) return `${p.toFixed(1)}% below average`
  return 'on par with average'
})

const categoryColors = {
  Bills: '#8b5cf6',
  Food: '#10b981',
}

const categoryChartData = (catTrend) => ({
  labels: catTrend.monthly_data.map(d => d.month),
  datasets: [{
    data: catTrend.monthly_data.map(d => d.amount),
    backgroundColor: categoryColors[catTrend.category_name] || '#8b5cf6',
    borderRadius: 4,
    barThickness: 12,
  }],
})

const miniChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#94a3b8',
      bodyColor: '#f8fafc',
      padding: 12,
      cornerRadius: 12,
      displayColors: false,
      callbacks: {
        label: (ctx) => ` Đ ${ctx.raw.toFixed(2)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: '#94a3b8', font: { size: 9 } },
    },
    y: {
      grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
      ticks: { display: false },
    },
  },
}

const loadStats = async () => {
  loading.value = true
  try {
    stats.value = await api.getStatistics(['Bills', 'Food'])
  } catch (error) {
    console.error('Error loading statistics:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadStats)
</script>

<template>
  <div class="py-4 flex flex-col gap-5">
    <header class="mb-1">
      <h2 class="text-3xl font-extrabold tracking-tighter text-brand-textMain">Statistics</h2>
    </header>

    <div v-if="loading" class="text-brand-textMuted text-sm py-8 text-center">Loading...</div>

    <template v-else-if="stats">
      <section class="bg-brand-surface p-5 rounded-app shadow-sm border border-white/5 flex flex-col items-center">
        <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">{{ stats.current_month }}</span>
        <h3 class="text-5xl font-extrabold tracking-tighter text-brand-textMain mt-1">
          Đ {{ stats.total_spent.toFixed(2) }}
        </h3>
        <div class="mt-3 flex items-center gap-1.5 text-sm font-medium"
             :class="vsAveragePercent > 0 ? 'text-red-400' : 'text-green-400'">
          <span>{{ vsAverageLabel }}</span>
        </div>
      </section>

      <section class="bg-brand-surface p-4 rounded-app shadow-sm border border-white/5 flex flex-col">
        <h3 class="text-sm font-semibold text-brand-textMuted mb-3">Yearly Trend</h3>
        <MonthlyChart :data="stats.monthly_trends" />
      </section>

      <section v-for="ct in stats.category_trends" :key="ct.category_name"
               class="bg-brand-surface p-4 rounded-app shadow-sm border border-white/5 flex flex-col">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-semibold text-brand-textMuted">{{ ct.category_name }}</h3>
          <span class="text-sm font-bold text-brand-textMain">
            Đ {{ ct.monthly_data.length > 0 ? ct.monthly_data[ct.monthly_data.length - 1].amount.toFixed(2) : '0.00' }}
          </span>
        </div>
        <div class="relative h-32">
          <Bar :data="categoryChartData(ct)" :options="miniChartOptions" />
        </div>
      </section>
    </template>
  </div>
</template>
