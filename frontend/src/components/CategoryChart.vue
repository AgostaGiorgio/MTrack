<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
  categories: {
    type: Array,
    required: true
  }
})

const chartData = computed(() => ({
  labels: props.categories.map(c => c.name),
  datasets: [
    {
      data: props.categories.map(c => c.amount),
      backgroundColor: props.categories.map(c => c.color),
      borderWidth: 0,
      hoverOffset: 4
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '85%',
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
        label: (context) => ` € ${context.raw.toFixed(2)}`
      }
    }
  }
}
</script>

<template>
  <div class="relative w-48 h-48">
    <Doughnut :data="chartData" :options="chartOptions" />
  </div>
</template>