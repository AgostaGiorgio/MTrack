<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip } from 'chart.js'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip)

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const chartData = computed(() => ({
  labels: props.data.map(d => d.month),
  datasets: [
    {
      data: props.data.map(d => d.amount),
      backgroundColor: '#8b5cf6', 
      borderRadius: 6, 
      barThickness: 16
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#94a3b8',
      bodyColor: '#f8fafc',
      padding: 12,
      cornerRadius: 12,
      displayColors: false,
      callbacks: {
        label: (context) => ` Đ ${context.raw.toFixed(2)}`
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false, 
        drawBorder: false
      },
      ticks: {
        color: '#94a3b8',
        font: { size: 10 }
      }
    },
    y: {
      grid: {
        color: 'rgba(255, 255, 255, 0.05)',
        drawBorder: false
      },
      ticks: {
        display: false
      }
    }
  }
}
</script>

<template>
  <div class="relative w-full h-48">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>