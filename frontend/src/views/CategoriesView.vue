<script setup>
import { ref, computed, onMounted } from 'vue'
import * as Icons from 'lucide-vue-next'

import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import BottomSheet from '../components/ui/BottomSheet.vue'
import InputField from '../components/ui/InputField.vue'
import LoadingSkeleton from '../components/ui/LoadingSkeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import IconPicker from '../components/IconPicker.vue'

const toast = useToast()

const categories = ref([])
const loading = ref(true)

const expandedCatId = ref(null)
const isSheetOpen = ref(false)
const sheetMode = ref('add-primary')
const formData = ref({ id: null, name: '', icon: 'Circle', parentId: null })
const saving = ref(false)

const titles = {
  'add-primary': 'New category',
  'edit-primary': 'Edit category',
  'add-secondary': 'New subcategory',
}

const sheetTitle = computed(() => titles[sheetMode.value] || 'Category')

const toggleAccordion = (id) => {
  expandedCatId.value = expandedCatId.value === id ? null : id
}

const openSheet = (mode, parentId = null, existingData = null) => {
  sheetMode.value = mode
  if (existingData) {
    formData.value = {
      id: existingData.id,
      name: existingData.name,
      icon: existingData.icon || 'Circle',
      parentId: null,
    }
  } else {
    formData.value = { id: null, name: '', icon: 'Circle', parentId }
  }
  isSheetOpen.value = true
}

const closeSheet = () => {
  isSheetOpen.value = false
}

const loadCategories = async () => {
  loading.value = true
  try {
    categories.value = await api.getCategories()
  } catch (error) {
    console.error('Failed to load categories:', error)
  } finally {
    loading.value = false
  }
}

const saveCategory = async () => {
  const name = formData.value.name.trim()
  if (!name) {
    toast.error('Enter a category name')
    return
  }

  const payload = {
    name,
    icon: formData.value.icon || 'Circle',
    ...(formData.value.parentId ? { parentId: formData.value.parentId } : {}),
  }

  saving.value = true
  try {
    if (formData.value.id) {
      await api.updateCategory({ id: formData.value.id, ...payload })
    } else {
      await api.addCategory(payload)
    }
    toast.success(
      formData.value.id
        ? 'Category updated'
        : formData.value.parentId
          ? 'Subcategory created'
          : 'Category created'
    )
    await loadCategories()
    closeSheet()
  } catch (error) {
    toast.error('Could not save the category')
    console.error('Failed to save category:', error)
  } finally {
    saving.value = false
  }
}

const deleteSubcategory = async (categoryId, subcategoryId) => {
  if (!window.confirm('Are you sure you want to delete this subcategory?')) return
  try {
    await api.unlinkSubCategory(categoryId, subcategoryId)
    toast.success('Subcategory removed')
    await loadCategories()
  } catch (error) {
    toast.error('Could not remove the subcategory')
    console.error('Failed to unlink subcategory:', error)
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-4 w-full">
      <div class="flex items-center justify-between px-1">
        <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Categories</h2>
        <button
          type="button"
          @click="openSheet('add-primary')"
          class="h-9 pl-3 pr-4 rounded-full bg-brand-primary text-white flex items-center gap-1.5 shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary active:scale-95 transition-all"
        >
          <Icons.Plus :size="16" :stroke-width="2.5" />
          <span class="text-xs font-bold whitespace-nowrap">Add category</span>
        </button>
      </div>

      <LoadingSkeleton v-if="loading" :lines="5" height="h-14" />

      <EmptyState
        v-else-if="categories.length === 0"
        :icon="Icons.Tags"
        title="No categories yet"
        description="Create your first category to start organizing expenses."
      >
        <button
          type="button"
          @click="openSheet('add-primary')"
          class="flex items-center gap-1.5 px-4 py-2 rounded-app-sm bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors"
        >
          <Icons.Plus :size="16" /> New category
        </button>
      </EmptyState>

      <section v-else class="app-card rounded-app overflow-hidden divide-y divide-white/5">
        <div v-for="cat in categories" :key="cat.id">
          <div
            @click="toggleAccordion(cat.id)"
            class="flex items-center gap-3 px-4 py-3 cursor-pointer hover:bg-white/[0.03] transition-colors"
          >
            <span
              class="w-9 h-9 rounded-full bg-brand-background border border-white/5 flex items-center justify-center shrink-0"
            >
              <component :is="Icons[cat.icon] || Icons.Circle" :size="16" class="text-brand-primary" />
            </span>

            <div class="flex flex-col min-w-0 flex-1 gap-0.5">
              <span class="text-brand-textMain font-semibold text-sm truncate">{{ cat.name }}</span>
              <span class="text-[11px] text-brand-textMuted">
                {{ cat.sub_categories?.length || 0 }}
                {{ (cat.sub_categories?.length || 0) === 1 ? 'subcategory' : 'subcategories' }}
              </span>
            </div>

            <button
              type="button"
              @click.stop="openSheet('edit-primary', null, cat)"
              class="w-8 h-8 rounded-full flex items-center justify-center text-brand-textMuted hover:text-brand-primary hover:bg-white/5 transition-colors shrink-0"
              title="Edit category"
            >
              <Icons.Edit2 :size="14" />
            </button>

            <component
              :is="expandedCatId === cat.id ? Icons.ChevronUp : Icons.ChevronDown"
              :size="16"
              class="text-brand-textMuted shrink-0"
            />
          </div>

          <div
            class="grid transition-[grid-template-rows,opacity] duration-300 ease-in-out"
            :class="expandedCatId === cat.id ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'"
          >
            <div class="overflow-hidden">
              <div class="px-4 pb-3">
                <div
                  v-if="cat.sub_categories?.length"
                  class="flex flex-col gap-1 ml-1 pl-4 border-l border-white/10"
                >
                  <div
                    v-for="sub in cat.sub_categories"
                    :key="sub.id"
                    class="flex items-center gap-3 py-1.5"
                  >
                    <span class="w-1.5 h-1.5 rounded-full bg-brand-primary/60 shrink-0" />
                    <span class="flex-1 text-brand-textMuted text-sm truncate">{{ sub.name }}</span>
                    <button
                      type="button"
                      @click="deleteSubcategory(cat.id, sub.id)"
                      class="w-7 h-7 rounded-full flex items-center justify-center text-brand-textMuted hover:text-red-400 hover:bg-white/5 transition-colors shrink-0"
                      title="Delete subcategory"
                    >
                      <Icons.Trash2 :size="13" />
                    </button>
                  </div>
                </div>

                <p v-else class="text-brand-textMuted text-xs py-2 pl-1">No subcategories</p>

                <button
                  type="button"
                  @click="openSheet('add-secondary', cat.id)"
                  class="flex items-center gap-1.5 text-brand-primary text-xs font-semibold py-1.5 hover:text-brand-secondary transition-colors"
                >
                  <Icons.Plus :size="14" /> Add subcategory
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <BottomSheet :open="isSheetOpen" :title="sheetTitle" @close="closeSheet">
      <div class="flex flex-col gap-5">
        <InputField
          v-model="formData.name"
          label="Name"
          placeholder="e.g. Health"
          hint="Shown on the dashboard and transactions."
        />

        <IconPicker v-if="sheetMode !== 'add-secondary'" v-model="formData.icon" />
      </div>

      <template #footer>
        <button
          type="button"
          :disabled="saving"
          @click="saveCategory"
          class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
        >
          {{ saving ? 'Saving…' : sheetMode === 'add-secondary' ? 'Create subcategory' : 'Save category' }}
        </button>
      </template>
    </BottomSheet>
  </main>
</template>
