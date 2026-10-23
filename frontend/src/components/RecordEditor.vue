<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { X, CreditCard, Trash2 } from 'lucide-vue-next'

import SelectField from './ui/SelectField.vue'
import InputField from './ui/InputField.vue'
import { formatDate } from '../utils/format'

const props = defineProps({
  open: { type: Boolean, default: false },
  transaction: { type: Object, default: null },
  categories: { type: Array, default: () => [] },
  saving: { type: Boolean, default: false },
  deleting: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'save', 'delete'])

const amount = ref('')
const recordDate = ref('')
const primaryId = ref('')
const secondaryId = ref('')
const amountError = ref('')
const dateError = ref('')
const confirmingDelete = ref(false)

const isBusy = computed(() => props.saving || props.deleting)
const formattedDate = computed(() =>
  recordDate.value ? formatDate(`${recordDate.value}T00:00:00`) : '—'
)

const primaryOptions = computed(() =>
  props.categories.map((category) => ({ value: category.id, label: category.name }))
)

const availableSubs = computed(() => {
  if (!primaryId.value) return []
  const category = props.categories.find((c) => String(c.id) === String(primaryId.value))
  return category ? category.sub_categories || [] : []
})

const secondaryOptions = computed(() => [
  { value: '', label: 'None' },
  ...availableSubs.value.map((sub) => ({ value: sub.id, label: sub.name })),
])

let previousBodyOverflow = ''

watch(
  () => props.transaction,
  (transaction) => {
    if (!transaction) return
    amount.value =
      transaction.amount !== null && transaction.amount !== undefined
        ? Number(transaction.amount).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 6,
            useGrouping: false,
          })
        : ''
    primaryId.value = transaction.primary_category ? transaction.primary_category.id : ''
    secondaryId.value = transaction.secondary_category ? transaction.secondary_category.id : ''
    recordDate.value = transaction.date ? String(transaction.date).slice(0, 10) : ''
    amountError.value = ''
    dateError.value = ''
    confirmingDelete.value = false
  },
  { immediate: true }
)

watch(amount, () => {
  if (amountError.value) amountError.value = ''
})

watch(recordDate, () => {
  if (dateError.value) dateError.value = ''
})

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      previousBodyOverflow = document.body.style.overflow
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = previousBodyOverflow
      confirmingDelete.value = false
    }
  },
  { immediate: true }
)

const onKeydown = (event) => {
  if (event.key === 'Escape' && props.open && !isBusy.value) requestClose()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = previousBodyOverflow
})

const requestClose = () => {
  if (!isBusy.value) emit('close')
}

const handlePrimaryChange = () => {
  secondaryId.value = ''
}

const submit = () => {
  if (isBusy.value) return

  const parsedAmount = Number(String(amount.value).replace(',', '.'))
  if (!Number.isFinite(parsedAmount) || parsedAmount <= 0) {
    amountError.value = 'Enter an amount greater than zero'
    return
  }

  if (!recordDate.value) {
    dateError.value = 'Select a date'
    return
  }

  emit('save', {
    amount: parsedAmount,
    date: recordDate.value,
    primary_category_id: primaryId.value || null,
    secondary_category_id: secondaryId.value || null,
  })
}

const confirmDelete = () => {
  if (!isBusy.value) emit('delete')
}
</script>

<template>
  <Teleport to="body">
    <Transition name="record-modal" appear>
      <div
        v-if="open"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6"
        role="dialog"
        aria-modal="true"
        aria-labelledby="record-editor-title"
      >
        <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" @click="requestClose" />

        <div
          class="record-modal-panel relative w-full max-w-md max-h-[90vh] bg-brand-background rounded-app shadow-app border border-white/10 flex flex-col overflow-hidden"
        >
          <!-- Header -->
          <header class="shrink-0 flex items-start justify-between gap-3 px-5 pt-5 pb-4 border-b border-white/5">
            <div class="flex flex-col gap-1 min-w-0">
              <span class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">
                Edit record
              </span>
              <h2
                id="record-editor-title"
                class="text-brand-textMain font-bold text-lg leading-snug break-words"
              >
                {{ transaction?.description || 'No description' }}
              </h2>
              <div class="flex items-center gap-1.5 text-[11px] text-brand-textMuted">
                <CreditCard :size="12" class="shrink-0" />
                <span class="truncate">{{ transaction?.card || 'Unknown card' }}</span>
                <span>•</span>
                <span class="shrink-0">{{ formattedDate }}</span>
              </div>
            </div>

            <button
              type="button"
              :disabled="isBusy"
              @click="requestClose"
              class="w-9 h-9 rounded-full flex items-center justify-center text-brand-textMuted bg-brand-surface/50 hover:text-brand-textMain hover:bg-brand-surface transition-colors shrink-0 disabled:opacity-50"
              title="Close"
            >
              <X :size="18" />
            </button>
          </header>

          <!-- Body -->
          <div class="flex-1 min-h-0 overflow-y-auto hide-scrollbar px-5 py-5 flex flex-col gap-5">
            <!-- Amount -->
            <div class="flex flex-col gap-1.5">
              <label for="record-amount" class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted">
                Amount
              </label>
              <div
                class="flex items-center gap-2 bg-brand-surface/60 border rounded-app-sm px-3.5 py-3 transition-colors"
                :class="amountError ? 'border-red-400/60' : 'border-white/10 focus-within:border-brand-primary'"
              >
                <span class="text-brand-primary text-lg font-bold">Đ</span>
                <input
                  id="record-amount"
                  v-model="amount"
                  type="number"
                  inputmode="decimal"
                  step="0.01"
                  min="0.01"
                  placeholder="0.00"
                  :disabled="isBusy"
                  :aria-invalid="!!amountError"
                  class="w-full bg-transparent text-2xl font-extrabold tracking-tight text-brand-textMain outline-none placeholder:text-brand-textMuted/30 disabled:opacity-60"
                />
              </div>
              <span v-if="amountError" class="text-[11px] text-red-400">{{ amountError }}</span>
            </div>

            <InputField
              v-model="recordDate"
              label="Date"
              type="date"
              :error="dateError"
              :disabled="isBusy"
            />

            <!-- Categories -->
            <div class="flex flex-col gap-3 pt-4 border-t border-white/5">
              <SelectField
                v-model="primaryId"
                label="Primary category"
                placeholder="Select category…"
                :options="primaryOptions"
                :disabled="isBusy"
                @change="handlePrimaryChange"
              />

              <SelectField
                v-if="availableSubs.length > 0"
                v-model="secondaryId"
                label="Secondary category"
                :options="secondaryOptions"
                hint="Optional"
                :disabled="isBusy"
              />
            </div>
          </div>

          <!-- Footer -->
          <footer
            class="shrink-0 px-5 pt-4 border-t border-white/5"
            style="padding-bottom: calc(1.25rem + env(safe-area-inset-bottom))"
          >
            <div v-if="confirmingDelete" class="flex flex-col gap-2">
              <p class="text-xs text-brand-textMuted text-center">
                Delete this record? This action cannot be undone.
              </p>
              <div class="flex gap-2">
                <button
                  type="button"
                  :disabled="isBusy"
                  @click="confirmingDelete = false"
                  class="flex-1 py-3 rounded-app-sm bg-brand-surface border border-white/10 text-brand-textMain text-sm font-semibold hover:bg-brand-surface/80 transition-colors disabled:opacity-60"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  :disabled="isBusy"
                  @click="confirmDelete"
                  class="flex-1 py-3 rounded-app-sm bg-red-500 text-white text-sm font-bold hover:bg-red-400 transition-colors disabled:opacity-60"
                >
                  {{ deleting ? 'Deleting…' : 'Delete' }}
                </button>
              </div>
            </div>

            <div v-else class="flex flex-col gap-2">
              <button
                type="button"
                :disabled="isBusy"
                @click="submit"
                class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
              >
                {{ saving ? 'Saving…' : 'Save changes' }}
              </button>

              <button
                type="button"
                :disabled="isBusy"
                @click="confirmingDelete = true"
                class="w-full flex items-center justify-center gap-1.5 py-3 rounded-app-sm text-red-400 text-sm font-semibold border border-red-400/20 bg-red-400/5 hover:bg-red-400/10 transition-colors disabled:opacity-60"
              >
                <Trash2 :size="15" />
                Delete record
              </button>
            </div>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.record-modal-enter-active,
.record-modal-leave-active {
  transition: opacity 0.2s ease;
}
.record-modal-enter-from,
.record-modal-leave-to {
  opacity: 0;
}
.record-modal-enter-active .record-modal-panel,
.record-modal-leave-active .record-modal-panel {
  transition:
    transform 0.24s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 0.2s ease;
}
.record-modal-enter-from .record-modal-panel,
.record-modal-leave-to .record-modal-panel {
  opacity: 0;
  transform: translateY(14px) scale(0.97);
}
</style>
