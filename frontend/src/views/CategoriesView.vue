<script setup>
import { ref, computed, onMounted } from 'vue'

import { api } from '../services/api'
import * as Icons from 'lucide-vue-next'
import BottomSheet from '../components/BottomSheet.vue'
import IconPicker from '../components/IconPicker.vue'


const categories = ref([])

const expandedCatId = ref(null)
const isSheetOpen = ref(false)
const sheetMode = ref('add-primary')
const formData = ref({ id: null, name: '', icon: 'Circle', parentId: null })
const iconSearch = ref('')

const toggleAccordion = (id) => expandedCatId.value = expandedCatId.value === id ? null : id

const openSheet = (mode, parentId = null, existingData = null) => {
  sheetMode.value = mode
  iconSearch.value = ''
  if (existingData) formData.value = { ...existingData }
  else formData.value = { id: null, name: '', icon: 'Circle', parentId }
  if (formData.value.icon === null) formData.value.icon = 'Circle'
  isSheetOpen.value = true
}
const closeSheet = () => isSheetOpen.value = false

const loadCategories = async () => {
  try {
    const [rawCategories] = await Promise.all([
      api.getCategories()
    ])
    categories.value = rawCategories
  } catch (error) {
    console.error("Errore fatale nel caricamento del carosello:", error)
  }
}

onMounted(() => {
  loadCategories()
})

const saveCategory = async () => {
  try {
    if (formData.value.id) {
      await api.updateCategory(formData.value)
    } else{
      await api.addCategory(formData.value)
    }
    await loadCategories()
  } catch (error) {
    console.error("Errore fatale nel salvataggio della categoria:", error)
  } finally {
    closeSheet()
  }
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

    <div class="flex flex-col gap-2 pb-24">
      <div v-for="cat in categories" :key="cat.id" class="bg-brand-surface rounded-app-sm shadow-sm border border-white/5 overflow-hidden">
        
        <div @click="toggleAccordion(cat.id)" class="py-2 px-4 flex justify-between items-center cursor-pointer">
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
            <component :is="expandedCatId === cat.id ? Icons.ChevronUp : Icons.ChevronDown" class="w-5 h-5 text-brand-textMuted transition-transform" />
          </div>
        </div>

        <div 
          class="grid transition-[grid-template-rows,opacity] duration-300 ease-in-out"
          :class="expandedCatId === cat.id ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'"
        >
          <div class="overflow-hidden">
            <div class="bg-brand-background/30 border-t border-white/5 py-2 px-3 flex flex-col gap-2">
              <div v-for="sub in cat.sub_categories" :key="sub.id" class="flex justify-between items-center p-2">
                <span class="text-brand-textMuted font-medium pl-2 border-l-2 border-brand-primary/50">{{ sub.name }}</span>
                <button class="p-1.5 text-brand-textMuted hover:text-red-400">
                  <Icons.Trash2 class="w-4 h-4" />
                </button>
              </div>
              <button @click="openSheet('add-secondary', cat.id)" class="flex items-center gap-2 text-sm text-brand-primary font-medium p-2 self-start">
                <Icons.Plus class="w-4 h-4" /> Add Subcategory
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <BottomSheet 
    :isOpen="isSheetOpen" 
    :title="sheetMode === 'add-primary' ? 'New Category' : 'Edit Category'"
    @close="closeSheet"
    >
      <div class="flex flex-col gap-5">
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-brand-textMuted uppercase tracking-wider">Name</label>
          <input v-model="formData.name" type="text" placeholder="e.g. Health" 
                  class="w-full bg-brand-background text-brand-textMain border border-white/10 rounded-xl p-4 focus:outline-none focus:border-brand-primary font-medium placeholder:text-white/20">
        </div>

        <IconPicker v-if="sheetMode !== 'add-secondary'" v-model="formData.icon" />

        <button @click="saveCategory" class="mt-4 w-full bg-brand-primary text-white font-bold py-4 rounded-xl shadow-lg hover:bg-brand-secondary shrink-0">
          Save Category
        </button>
      </div>
    </BottomSheet>
  </div>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>