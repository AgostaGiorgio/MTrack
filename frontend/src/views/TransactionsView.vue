<script setup>
import { ref, computed, onMounted } from 'vue'
import { ChevronLeft, ChevronRight, Receipt } from '@lucide/vue'
import * as Icons from '@lucide/vue'

import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import TransactionItem from '../components/TransactionItem.vue'
import RecordEditor from '../components/RecordEditor.vue'
import LoadingSkeleton from '../components/ui/LoadingSkeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'

const toast = useToast()

const transactions = ref([])
const categories = ref([])
const selectedCategoryId = ref(null)
const loading = ref(true)

const getCurrentMtrackMonth = () => {
  const now = new Date()
  const day = now.getDate()
  if (day < 3) {
    const prev = new Date(now.getFullYear(), now.getMonth(), 0)
    return { year: prev.getFullYear(), month: prev.getMonth() + 1 }
  }
  return { year: now.getFullYear(), month: now.getMonth() + 1 }
}

const currentMtrack = getCurrentMtrackMonth()
const viewYear = ref(currentMtrack.year)
const viewMonth = ref(currentMtrack.month)

const viewMonthLabel = computed(() => {
  const date = new Date(viewYear.value, viewMonth.value - 1)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const isCurrentMonth = computed(
  () => viewYear.value === currentMtrack.year && viewMonth.value === currentMtrack.month
)

const goPrevMonth = () => {
  if (viewMonth.value === 1) {
    viewMonth.value = 12
    viewYear.value -= 1
  } else {
    viewMonth.value -= 1
  }
  loadTransactionsData()
}

const goNextMonth = () => {
  if (isCurrentMonth.value) return
  if (viewMonth.value === 12) {
    viewMonth.value = 1
    viewYear.value += 1
  } else {
    viewMonth.value += 1
  }
  loadTransactionsData()
}

const filteredTransactions = computed(() => {
  if (!selectedCategoryId.value) return transactions.value
  return transactions.value.filter((tx) => {
    const catId = tx.primary_category?.id
    return catId && String(catId) === String(selectedCategoryId.value)
  })
})

const filterCategories = computed(() => {
  const seen = new Set()
  const cats = []
  for (const tx of transactions.value) {
    if (tx.primary_category && !seen.has(tx.primary_category.id)) {
      seen.add(tx.primary_category.id)
      cats.push(tx.primary_category)
    }
  }
  return cats
})

const editingTx = ref(null)
const isEditorOpen = ref(false)
const saving = ref(false)
const deleting = ref(false)

const isAddMode = computed(() => !editingTx.value)

const getCategoryIcon = (category) => {
  if (!category) return Icons.Circle

  const cat = categories.value.find((c) => c.id === category.id)
  const iconName = cat && cat.icon ? cat.icon : 'Circle'

  return Icons[iconName] || Icons.Circle
}

const openEditor = (tx) => {
  editingTx.value = { ...tx }
  isEditorOpen.value = true
}

const openAddEditor = () => {
  editingTx.value = null
  isEditorOpen.value = true
}

const closeEditor = () => {
  isEditorOpen.value = false
  editingTx.value = null
}

const handleSave = async (payload) => {
  saving.value = true
  try {
    if (isAddMode.value) {
      await api.addTransaction(payload)
      toast.success('Record added')
    } else {
      await api.updateTransaction(editingTx.value.id, payload)
      toast.success('Record updated')
    }
    await loadTransactionsData()
    closeEditor()
  } catch (error) {
    toast.error(isAddMode.value ? 'Could not add the record' : 'Could not update the record')
    console.error('Failed to save transaction:', error)
  } finally {
    saving.value = false
  }
}

const handleDelete = async () => {
  if (!editingTx.value) return

  deleting.value = true
  try {
    await api.deleteTransaction(editingTx.value.id)
    toast.success('Record deleted')
    await loadTransactionsData()
    closeEditor()
  } catch (error) {
    toast.error('Could not delete the record')
    console.error('Failed to delete transaction:', error)
  } finally {
    deleting.value = false
  }
}

const loadTransactionsData = async () => {
  loading.value = true
  try {
    const params = {}
    if (viewYear.value) params.year = viewYear.value
    if (viewMonth.value) params.month = viewMonth.value
    const [rawTransactionsData, rawCategoriesData] = await Promise.all([
      api.getTransactions(params),
      api.getCategories(),
    ])

    transactions.value = rawTransactionsData
    categories.value = rawCategoriesData
    selectedCategoryId.value = null
  } catch (error) {
    console.error('Failed to load transactions or categories:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTransactionsData()
})
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-4 w-full">
      <!-- Month navigation -->
      <section class="app-card rounded-app px-3 py-2 flex items-center justify-between">
        <button
          type="button"
          @click="goPrevMonth"
          class="w-9 h-9 rounded-full flex items-center justify-center text-brand-textMuted hover:text-brand-textMain hover:bg-white/5 transition-colors"
        >
          <ChevronLeft :size="18" />
        </button>

        <span class="text-sm font-semibold text-brand-textMain">{{ viewMonthLabel }}</span>

        <button
          type="button"
          @click="goNextMonth"
          :disabled="isCurrentMonth"
          class="w-9 h-9 rounded-full flex items-center justify-center transition-colors"
          :class="isCurrentMonth ? 'text-brand-textMuted opacity-30 cursor-not-allowed' : 'text-brand-textMuted hover:text-brand-textMain hover:bg-white/5'"
        >
          <ChevronRight :size="18" />
        </button>
      </section>

      <!-- Category filter -->
      <div class="flex gap-2 overflow-x-auto hide-scrollbar pb-1">
        <button
          type="button"
          @click="selectedCategoryId = null"
          class="shrink-0 px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors border"
          :class="selectedCategoryId === null ? 'bg-brand-primary text-white border-transparent shadow-sm' : 'bg-brand-surface/60 text-brand-textMuted border-white/5 hover:text-brand-textMain'"
        >
          All
        </button>
        <button
          v-for="cat in filterCategories"
          :key="cat.id"
          type="button"
          @click="selectedCategoryId = cat.id"
          class="shrink-0 px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors border"
          :class="selectedCategoryId === cat.id ? 'bg-brand-primary text-white border-transparent shadow-sm' : 'bg-brand-surface/60 text-brand-textMuted border-white/5 hover:text-brand-textMain'"
        >
          {{ cat.name }}
        </button>
      </div>

      <div class="flex items-center justify-between px-1">
        <span class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">
          Records
        </span>
        <button
          type="button"
          @click="openAddEditor"
          class="text-[11px] font-semibold text-brand-primary hover:text-brand-secondary transition-colors"
        >
          + Add record
        </button>
      </div>

      <LoadingSkeleton v-if="loading" :lines="5" height="h-16" />

      <EmptyState
        v-else-if="filteredTransactions.length === 0"
        :icon="Receipt"
        title="No records"
        :description="transactions.length === 0 ? 'No transactions for this month.' : 'No transactions for this category.'"
      />

      <section v-else class="app-card rounded-app overflow-hidden divide-y divide-white/5">
        <TransactionItem
          v-for="tx in filteredTransactions"
          :key="tx.id"
          :transaction="tx"
          :icon-component="getCategoryIcon(tx.primary_category)"
          @edit="openEditor"
        />
      </section>
    </div>

    <RecordEditor
      :open="isEditorOpen"
      :transaction="editingTx"
      :categories="categories"
      :saving="saving"
      :deleting="deleting"
      @close="closeEditor"
      @save="handleSave"
      @delete="handleDelete"
    />
  </main>
</template>
