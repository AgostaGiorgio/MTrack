<script setup>
import { ref, computed } from 'vue'
import * as Icons from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: String, required: true }
})
const emit = defineEmits(['update:modelValue'])

const allIconNames = Object.keys(Icons).filter(key => /^[A-Z]/.test(key) && key !== 'createLucideIcon')
const iconSearch = ref('')

const displayedIcons = computed(() => {
  const query = iconSearch.value.toLowerCase()
  if (!query) return allIconNames.slice(0, 60)
  return allIconNames.filter(name => name.toLowerCase().includes(query)).slice(0, 60)
})

const selectIcon = (iconName) => {
  emit('update:modelValue', iconName)
}
</script>

<template>
  <div class="flex flex-col gap-2 mt-2">
    <div class="flex justify-between items-center mb-1">
      <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Select Icon</label>
      <div class="flex items-center gap-2">
        <span class="text-xs text-brand-textMuted">Selected:</span>
        <component :is="Icons[modelValue] || Icons.Circle" class="w-4 h-4 text-brand-primary" />
      </div>
    </div>
    
    <div class="relative mb-2">
      <Icons.Search class="w-4 h-4 absolute left-3 top-3.5 text-brand-textMuted" />
      <input v-model="iconSearch" type="text" placeholder="Search icons..." 
             class="w-full bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-3 pl-9 text-sm focus:outline-none focus:border-brand-primary">
    </div>

    <div class="grid grid-cols-6 gap-2 h-48 overflow-y-auto p-1 hide-scrollbar content-start">
      <button v-for="iconName in displayedIcons" :key="iconName"
              @click="selectIcon(iconName)"
              class="aspect-square rounded-xl flex items-center justify-center border transition-all"
              :class="modelValue === iconName ? 'bg-brand-primary/20 border-brand-primary text-brand-primary' : 'bg-brand-background border-white/5 text-brand-textMuted hover:border-white/20'">
        <component :is="Icons[iconName]" class="w-5 h-5" />
      </button>
      
      <div v-if="displayedIcons.length === 0" class="col-span-6 flex flex-col items-center justify-center h-full text-brand-textMuted opacity-50 pt-8">
        <Icons.SearchX class="w-8 h-8 mb-2" />
        <span class="text-sm">No icons found</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>