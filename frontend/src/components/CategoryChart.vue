<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'
import { formatMoney } from '../utils/format'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
  categories: {
    type: Array,
    required: true,
  },
})

const chartData = computed(() => ({
  labels: props.categories.map((c) => c.name),
  datasets: [
    {
      data: props.categories.map((c) => c.amount),
      backgroundColor: props.categories.map((c) => c.color),
      borderWidth: 0,
      hoverOffset: 4,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '68%',
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
        label: (context) => ` ${formatMoney(context.raw)}`,
      },
    },
  },
}
</script>

<template>
  <div class="relative w-40 h-40">
    <Doughnut :data="chartData" :options="chartOptions" />
  </div>
</template>
