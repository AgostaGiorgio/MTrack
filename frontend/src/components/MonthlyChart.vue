<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'
import { formatMoney } from '../utils/format'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip)

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
})

const chartData = computed(() => ({
  labels: props.data.map((d) => d.month),
  datasets: [
    {
      data: props.data.map((d) => d.amount),
      backgroundColor: '#8b5cf6',
      hoverBackgroundColor: '#c084fc',
      borderRadius: 4,
      maxBarThickness: 34,
    },
  ],
}))

const chartOptions = {
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
        label: (context) => ` ${formatMoney(context.raw)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      border: { display: false },
      ticks: { color: '#94a3b8', font: { size: 10 }, maxRotation: 0, autoSkip: true },
    },
    y: {
      grid: { color: 'rgba(255, 255, 255, 0.05)' },
      border: { display: false },
      ticks: { display: false },
    },
  },
}
</script>

<template>
  <div class="relative w-full h-44">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
