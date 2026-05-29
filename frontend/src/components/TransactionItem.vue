<script setup>
import { computed } from 'vue'
import * as Icons from 'lucide-vue-next'

const props = defineProps({
  transaction: { type: Object, required: true },
  iconComponent: { type: [Object, Function], required: true }
})

defineEmits(['edit'])

const formattedDate = computed(() => {
  return new Date(props.transaction.date).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
})
</script>

<template>
  <div class="bg-brand-surface p-4 rounded-app-sm shadow-sm border border-white/5 flex flex-col gap-3">
    
    <div class="flex justify-between items-start">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-brand-background flex items-center justify-center flex-shrink-0">
          <component :is="iconComponent" class="w-5 h-5 text-brand-primary" />
        </div>
        <div>
          <div class="text-brand-textMain font-bold text-base leading-tight">{{ transaction.description }}</div>
          <div class="flex items-center gap-1 text-xs text-brand-textMuted mt-1">
            <Icons.CreditCard class="w-3 h-3" />
            <span>{{ transaction.card }}</span>
            <span class="mx-1">•</span>
            <span>{{ formattedDate }}</span>
          </div>
        </div>
      </div>
      <div class="text-brand-textMain font-extrabold">
        Đ {{ transaction.amount.toFixed(2) }}
      </div>
    </div>

    <div class="mt-1 pt-3 border-t border-white/5">
      <button @click="$emit('edit', transaction)" 
              class="w-full flex items-center justify-between bg-brand-background/50 hover:bg-brand-background/80 transition-colors p-2.5 rounded-lg border border-white/5">
        <div class="flex items-center gap-2 text-sm">
          <span class="font-medium" :class="transaction.primary_category ? 'text-brand-primary' : 'text-brand-textMuted'">
            {{ transaction.primary_category?.name || 'Uncategorized' }}
          </span>
          <span v-if="transaction.secondary_category" class="text-brand-textMuted text-xs">/</span>
          <span v-if="transaction.secondary_category" class="text-brand-textMuted text-xs font-medium">{{ transaction.secondary_category.name }}</span>
        </div>
        <div class="flex items-center gap-2 text-xs text-brand-textMuted">
          <span>Edit</span>
          <Icons.ChevronRight class="w-4 h-4" />
        </div>
      </button>
    </div>
    
  </div>
</template>