<script setup>
import { computed } from 'vue'
import * as Icons from 'lucide-vue-next'
import MoneyValue from './ui/MoneyValue.vue'
import { formatDate } from '../utils/format'

const props = defineProps({
  transaction: { type: Object, required: true },
  iconComponent: { type: [Object, Function], required: true },
})

defineEmits(['edit'])

const formattedDate = computed(() => formatDate(props.transaction.date))
</script>

<template>
  <button
    type="button"
    @click="$emit('edit', transaction)"
    class="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-white/[0.03] active:bg-white/[0.05] transition-colors"
  >
    <span
      class="w-9 h-9 rounded-full bg-brand-background border border-white/5 flex items-center justify-center shrink-0"
    >
      <component :is="iconComponent" :size="16" class="text-brand-primary" />
    </span>

    <span class="flex flex-col min-w-0 flex-1 gap-0.5">
      <span class="text-brand-textMain font-semibold text-sm truncate">
        {{ transaction.description || 'No description' }}
      </span>

      <span class="flex items-center gap-1 text-[11px] text-brand-textMuted">
        <Icons.CreditCard :size="11" class="shrink-0" />
        <span class="truncate">{{ transaction.card || 'Unknown card' }}</span>
        <span class="mx-0.5">•</span>
        <span class="shrink-0">{{ formattedDate }}</span>
      </span>

      <span class="flex items-center gap-1 text-[11px] font-medium truncate">
        <span v-if="transaction.primary_category" class="text-brand-primary truncate">
          {{ transaction.primary_category.name }}
        </span>
        <span v-else class="text-brand-textMuted italic">Uncategorized</span>

        <template v-if="transaction.secondary_category">
          <span class="text-brand-textMuted">/</span>
          <span class="text-brand-textMuted truncate">{{ transaction.secondary_category.name }}</span>
        </template>
      </span>
    </span>

    <span class="flex flex-col items-end shrink-0 gap-0.5">
      <MoneyValue :value="transaction.amount" class="text-brand-textMain font-bold text-sm" />
      <span class="flex items-center gap-0.5 text-[10px] text-brand-textMuted">
        Edit
        <Icons.ChevronRight :size="12" />
      </span>
    </span>
  </button>
</template>
