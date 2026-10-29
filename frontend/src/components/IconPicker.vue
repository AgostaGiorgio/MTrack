<script setup>
import { ref, computed } from 'vue'
import * as Icons from 'lucide-vue-next'

defineProps({
  modelValue: { type: String, required: true },
})
const emit = defineEmits(['update:modelValue'])

const allIconNames = Object.keys(Icons).filter(
  (key) => /^[A-Z]/.test(key) && key !== 'createLucideIcon' && !key.endsWith('Icon')
)
const iconSearch = ref('')

const displayedIcons = computed(() => {
  const query = iconSearch.value.toLowerCase()
  if (!query) return allIconNames.slice(0, 60)
  return allIconNames.filter((name) => name.toLowerCase().includes(query)).slice(0, 60)
})

const selectIcon = (iconName) => {
  emit('update:modelValue', iconName)
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex justify-between items-center">
      <label class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted">Icon</label>
      <div class="flex items-center gap-1.5">
        <span class="text-[11px] text-brand-textMuted">Selected</span>
        <span class="w-6 h-6 rounded-full bg-brand-surface border border-white/10 flex items-center justify-center">
          <component :is="Icons[modelValue] || Icons.Circle" :size="13" class="text-brand-primary" />
        </span>
      </div>
    </div>

    <div class="relative">
      <Icons.Search :size="15" class="absolute left-3 top-1/2 -translate-y-1/2 text-brand-textMuted" />
      <input
        v-model="iconSearch"
        type="text"
        placeholder="Search icons…"
        class="w-full bg-brand-background text-brand-textMain border border-white/10 rounded-app-sm py-2.5 pl-9 pr-3 text-sm focus:outline-none focus:border-brand-primary placeholder:text-brand-textMuted/40"
      />
    </div>

    <div class="grid grid-cols-6 gap-2 h-48 overflow-y-auto p-1 hide-scrollbar content-start">
      <button
        v-for="iconName in displayedIcons"
        :key="iconName"
        type="button"
        @click="selectIcon(iconName)"
        class="aspect-square rounded-app-sm flex items-center justify-center border transition-all"
        :class="modelValue === iconName
          ? 'bg-brand-primary/20 border-brand-primary text-brand-primary'
          : 'bg-brand-background border-white/5 text-brand-textMuted hover:border-white/20 hover:text-brand-textMain'"
      >
        <component :is="Icons[iconName]" :size="18" />
      </button>

      <div
        v-if="displayedIcons.length === 0"
        class="col-span-6 flex flex-col items-center justify-center h-full text-brand-textMuted opacity-50 pt-8"
      >
        <Icons.SearchX :size="28" class="mb-2" />
        <span class="text-sm">No icons found</span>
      </div>
    </div>
  </div>
</template>
