<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'

// Registriamo solo i moduli di Chart.js che ci servono per la ciambella
ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
  categories: {
    type: Array,
    required: true
  }
})

// Formattiamo i dati nel modo in cui se li aspetta Chart.js
const chartData = computed(() => ({
  labels: props.categories.map(c => c.name),
  datasets: [
    {
      data: props.categories.map(c => c.amount),
      backgroundColor: props.categories.map(c => c.color),
      borderWidth: 0, // Niente bordi per far risaltare i colori sul fondo scuro
      hoverOffset: 4
    }
  ]
}))

// Configurazioni per un look minimale ed elegante
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '85%', // Rende lo spessore della ciambella molto sottile
  plugins: {
    legend: {
      display: false // Nascondiamo la legenda nativa (usiamo quella custom HTML)
    },
    tooltip: {
      backgroundColor: '#1e293b', // brand-surface
      titleColor: '#94a3b8', // brand-textMuted
      bodyColor: '#f8fafc', // brand-textMain
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