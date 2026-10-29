import { ref } from 'vue'

// Shared module-level toast state (singleton).
const toasts = ref([])
let seq = 0

export function useToast() {
  const push = (message, type = 'info', timeout = 3000) => {
    const id = ++seq
    toasts.value.push({ id, message, type })
    if (timeout > 0) {
      setTimeout(() => dismiss(id), timeout)
    }
    return id
  }

  const dismiss = (id) => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts,
    dismiss,
    push,
    success: (m, t) => push(m, 'success', t),
    error: (m, t) => push(m, 'error', t ?? 4500),
    info: (m, t) => push(m, 'info', t),
  }
}
