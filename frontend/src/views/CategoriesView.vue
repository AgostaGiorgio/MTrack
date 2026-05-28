<script setup>
import { ref, computed } from 'vue'
import * as Icons from 'lucide-vue-next'

const allIconNames = Object.keys(Icons).filter(key => /^[A-Z]/.test(key) && key !== 'createLucideIcon')

const categories = ref([
  { id: '1', name: 'Car', icon: 'Car', type: 'primary', subs: [{ id: '1a', name: 'Fuel', type: 'secondary' }] },
  { id: '2', name: 'Utilities', icon: 'Zap', type: 'primary', subs: [{ id: '2a', name: 'Internet', type: 'secondary' }] }
])

const expandedCatId = ref(null)
const toggleAccordion = (id) => expandedCatId.value = expandedCatId.value === id ? null : id

const isSheetOpen = ref(false)
const sheetMode = ref('add-primary')
const formData = ref({ id: null, name: '', icon: 'CircleDollarSign', parentId: null })

const openSheet = (mode, parentId = null, existingData = null) => {
  sheetMode.value = mode
  iconSearch.value = ''
  if (existingData) formData.value = { ...existingData }
  else formData.value = { id: null, name: '', icon: 'CircleDollarSign', parentId }
  isSheetOpen.value = true
}
const closeSheet = () => isSheetOpen.value = false

const iconSearch = ref('')

const displayedIcons = computed(() => {
  const query = iconSearch.value.toLowerCase()
  if (!query) return allIconNames.slice(0, 60)
  return allIconNames.filter(name => name.toLowerCase().includes(query)).slice(0, 60)
})

const saveCategory = () => {
  console.log('Salvataggio nel DB...', formData.value)
  closeSheet()
}
</script>

<template>
  <div class="py-4 flex flex-col h-full">
    
    <header class="mb-6 mt-2 flex justify-between items-end">
      <div>
        <h2 class="text-3xl font-extrabold tracking-tighter text-brand-textMain">Categories</h2>
        <p class="text-sm text-brand-textMuted mt-1">Manage your tracking structure</p>
      </div>
      <button @click="openSheet('add-primary')" class="w-10 h-10 bg-brand-primary rounded-full flex items-center justify-center shadow-lg hover:bg-brand-secondary text-white">
        <Icons.Plus class="w-6 h-6" />
      </button>
    </header>

    <div class="flex flex-col gap-3 pb-24">
      <div v-for="cat in categories" :key="cat.id" class="bg-brand-surface rounded-app-sm shadow-sm border border-white/5 overflow-hidden">
        
        <div @click="toggleAccordion(cat.id)" class="p-4 flex justify-between items-center cursor-pointer">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-full bg-brand-background flex items-center justify-center">
              <component :is="Icons[cat.icon] || Icons.Circle" class="w-5 h-5 text-brand-primary" />
            </div>
            <span class="text-brand-textMain font-bold text-lg">{{ cat.name }}</span>
          </div>
          <div class="flex items-center gap-3">
            <button @click.stop="openSheet('edit-primary', null, cat)" class="p-2 text-brand-textMuted">
              <Icons.Edit2 class="w-4 h-4" />
            </button>
            <component :is="expandedCatId === cat.id ? Icons.ChevronUp : Icons.ChevronDown" class="w-5 h-5 text-brand-textMuted" />
          </div>
        </div>

        <transition enter-active-class="transition-all duration-200" leave-active-class="transition-all duration-150" enter-from-class="max-h-0 opacity-0" leave-to-class="max-h-0 opacity-0">
          <div v-if="expandedCatId === cat.id" class="bg-brand-background/30 border-t border-white/5 p-4 flex flex-col gap-2 overflow-hidden">
            <div v-for="sub in cat.subs" :key="sub.id" class="flex justify-between items-center p-2">
              <span class="text-brand-textMuted font-medium pl-2 border-l-2 border-brand-primary/50">{{ sub.name }}</span>
              <button class="p-1.5 text-brand-textMuted hover:text-red-400"><Icons.Trash2 class="w-4 h-4" /></button>
            </div>
            <button @click="openSheet('add-secondary', cat.id)" class="mt-2 flex items-center gap-2 text-sm text-brand-primary font-medium p-2 self-start">
              <Icons.Plus class="w-4 h-4" /> Add Subcategory
            </button>
          </div>
        </transition>
      </div>
    </div>

    <Teleport to="body">
      <transition enter-active-class="transition-opacity duration-300" leave-active-class="transition-opacity duration-300" enter-from-class="opacity-0" leave-to-class="opacity-0">
        <div v-if="isSheetOpen" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60]" @click="closeSheet"></div>
      </transition>

      <transition enter-active-class="transition-transform duration-300" leave-active-class="transition-transform duration-300" enter-from-class="translate-y-full" leave-to-class="translate-y-full">
        <div v-if="isSheetOpen" class="fixed bottom-0 left-0 w-full max-h-[90vh] flex flex-col bg-brand-surface rounded-t-app shadow-app border-t border-white/10 z-[70]">
          
          <div class="p-6 pb-2 shrink-0 flex justify-between items-center">
            <h3 class="text-xl font-bold text-brand-textMain">
              {{ sheetMode === 'add-primary' ? 'New Category' : sheetMode === 'add-secondary' ? 'New Subcategory' : 'Edit Category' }}
            </h3>
            <button @click="closeSheet" class="w-8 h-8 rounded-full bg-brand-background flex items-center justify-center text-brand-textMuted">
              <Icons.X class="w-5 h-5" />
            </button>
          </div>

          <div class="p-6 pt-4 overflow-y-auto flex flex-col gap-5">
            <div class="flex flex-col gap-2">
              <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Name</label>
              <input v-model="formData.name" type="text" placeholder="e.g. Health" 
                     class="w-full bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-4 focus:outline-none focus:border-brand-primary font-medium placeholder:text-white/20">
            </div>

            <div v-if="sheetMode !== 'add-secondary'" class="flex flex-col gap-2 mt-2">
              <div class="flex justify-between items-center mb-1">
                <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Select Icon</label>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-brand-textMuted">Selected:</span>
                  <component :is="Icons[formData.icon] || Icons.Circle" class="w-4 h-4 text-brand-primary" />
                </div>
              </div>
              
              <div class="relative mb-2">
                <Icons.Search class="w-4 h-4 absolute left-3 top-3.5 text-brand-textMuted" />
                <input v-model="iconSearch" type="text" placeholder="Search icons (e.g. heart, game)..." 
                       class="w-full bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-3 pl-9 text-sm focus:outline-none focus:border-brand-primary">
              </div>

              <div class="grid grid-cols-6 gap-2 h-48 overflow-y-auto p-1 hide-scrollbar content-start">
                <button v-for="iconName in displayedIcons" :key="iconName"
                        @click="formData.icon = iconName"
                        class="aspect-square rounded-xl flex items-center justify-center border transition-all"
                        :class="formData.icon === iconName ? 'bg-brand-primary/20 border-brand-primary text-brand-primary' : 'bg-brand-background border-white/5 text-brand-textMuted hover:border-white/20'">
                  <component :is="Icons[iconName]" class="w-5 h-5" />
                </button>
              </div>
            </div>

            <button @click="saveCategory" class="mt-4 w-full bg-brand-primary text-white font-bold py-4 rounded-xl shadow-lg hover:bg-brand-secondary shrink-0">
              Save Category
            </button>
          </div>

        </div>
      </transition>
    </Teleport>
  </div>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>