<script setup>
import { computed } from 'vue'
import { formatMoney, formatSignedMoney } from '../../utils/format'

const props = defineProps({
  value: { type: [Number, String], default: null },
  decimals: { type: Number, default: 2 },
  signed: { type: Boolean, default: false },
})

const display = computed(() =>
  props.signed ? formatSignedMoney(props.value, props.decimals) : formatMoney(props.value, props.decimals)
)
</script>

<template>
  <span class="tabular-nums whitespace-nowrap">{{ display }}</span>
</template>
