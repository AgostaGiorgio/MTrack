<script setup>
import { ref, computed, onMounted } from 'vue'
import * as Icons from 'lucide-vue-next'

import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import TransactionItem from '../components/TransactionItem.vue'
import BottomSheet from '../components/ui/BottomSheet.vue'
import SelectField from '../components/ui/SelectField.vue'
import LoadingSkeleton from '../components/ui/LoadingSkeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import MoneyValue from '../components/ui/MoneyValue.vue'

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
const editingTxPrimaryId = ref('')
const editingTxSecondaryId = ref('')
const saving = ref(false)

const primaryOptions = computed(() =>
  categories.value.map((category) => ({ value: category.id, label: category.name }))
)

const availableSubs = computed(() => {
  if (!editingTx.value || !editingTxPrimaryId.value) return []
  const cat = categories.value.find((c) => String(c.id) === String(editingTxPrimaryId.value))
  return cat ? cat.sub_categories || [] : []
})

const secondaryOptions = computed(() => [
  { value: '', label: 'None' },
  ...availableSubs.value.map((sub) => ({ value: sub.id, label: sub.name })),
])

const getCategoryIcon = (category) => {
  if (!category) return Icons.Circle

  const cat = categories.value.find((c) => c.id === category.id)
  const iconName = cat && cat.icon ? cat.icon : 'Circle'

  return Icons[iconName] || Icons.Circle
}

const openSheet = (tx) => {
  editingTx.value = { ...tx }
  editingTxPrimaryId.value = tx.primary_category ? tx.primary_category.id : ''
  editingTxSecondaryId.value = tx.secondary_category ? tx.secondary_category.id : ''
}

const closeSheet = () => {
  editingTx.value = null
  editingTxPrimaryId.value = ''
  editingTxSecondaryId.value = ''
}

const saveCategories = async () => {
  if (!editingTx.value) return

  const pcat = categories.value.find((c) => String(c.id) === String(editingTxPrimaryId.value))
  if (!pcat) {
    toast.error('Select a primary category')
    return
  }

  const scat = editingTxSecondaryId.value
    ? (pcat.sub_categories || []).find((c) => String(c.id) === String(editingTxSecondaryId.value))
    : null

  saving.value = true
  try {
    await api.updateTransactionCategories(editingTx.value.id, pcat.id, scat?.id)
    toast.success('Categories updated')
    await loadTransactionsData()
    closeSheet()
  } catch (error) {
    toast.error('Could not update the transaction')
    console.error('Failed to update transaction categories:', error)
  } finally {
    saving.value = false
  }
}

const handlePrimaryChange = () => {
  editingTxSecondaryId.value = ''
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
          <Icons.ChevronLeft :size="18" />
        </button>

        <span class="text-sm font-semibold text-brand-textMain">{{ viewMonthLabel }}</span>

        <button
          type="button"
          @click="goNextMonth"
          :disabled="isCurrentMonth"
          class="w-9 h-9 rounded-full flex items-center justify-center transition-colors"
          :class="isCurrentMonth ? 'text-brand-textMuted opacity-30 cursor-not-allowed' : 'text-brand-textMuted hover:text-brand-textMain hover:bg-white/5'"
        >
          <Icons.ChevronRight :size="18" />
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
        <span class="text-[11px] font-semibold text-brand-textMuted">
          {{ filteredTransactions.length }} records
        </span>
      </div>

      <LoadingSkeleton v-if="loading" :lines="5" height="h-16" />

      <EmptyState
        v-else-if="filteredTransactions.length === 0"
        :icon="Icons.Receipt"
        title="No records"
        :description="transactions.length === 0 ? 'No transactions for this month.' : 'No transactions for this category.'"
      />

      <section v-else class="app-card rounded-app overflow-hidden divide-y divide-white/5">
        <TransactionItem
          v-for="tx in filteredTransactions"
          :key="tx.id"
          :transaction="tx"
          :icon-component="getCategoryIcon(tx.primary_category)"
          @edit="openSheet"
        />
      </section>
    </div>

    <BottomSheet :open="!!editingTx" title="Assign category" @close="closeSheet">
      <div class="flex flex-col gap-5">
        <div class="flex justify-between items-center gap-3 p-3 bg-brand-surface/60 rounded-app-sm border border-white/5">
          <span class="text-brand-textMuted text-sm truncate">{{ editingTx?.description || 'No description' }}</span>
          <MoneyValue :value="editingTx?.amount" class="text-brand-textMain font-bold text-sm shrink-0" />
        </div>

        <SelectField
          v-model="editingTxPrimaryId"
          label="Primary category"
          placeholder="Select category…"
          :options="primaryOptions"
          @change="handlePrimaryChange"
        />

        <SelectField
          v-if="availableSubs.length > 0"
          v-model="editingTxSecondaryId"
          label="Secondary category"
          :options="secondaryOptions"
          hint="Optional"
        />
      </div>

      <template #footer>
        <button
          type="button"
          :disabled="saving || !editingTxPrimaryId"
          @click="saveCategories"
          class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
        >
          {{ saving ? 'Saving…' : 'Save changes' }}
        </button>
      </template>
    </BottomSheet>
  </main>
</template>
