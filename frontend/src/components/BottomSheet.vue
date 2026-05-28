<script setup>
import { X } from 'lucide-vue-next'

defineProps({
  isOpen: { type: Boolean, required: true },
  title: { type: String, required: true }
})

defineEmits(['close'])
</script>

<template>
  <Teleport to="body">
    <transition enter-active-class="transition-opacity duration-300" leave-active-class="transition-opacity duration-300" enter-from-class="opacity-0" leave-to-class="opacity-0">
      <div v-if="isOpen" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60]" @click="$emit('close')"></div>
    </transition>

    <transition enter-active-class="transition-transform duration-300" leave-active-class="transition-transform duration-300" enter-from-class="translate-y-full" leave-to-class="translate-y-full">
      <div v-if="isOpen" class="fixed bottom-0 left-0 w-full max-h-[90vh] flex flex-col bg-brand-surface rounded-t-app shadow-app border-t border-white/10 z-[70]">
        
        <div class="p-6 pb-2 shrink-0 flex justify-between items-center">
          <h3 class="text-xl font-bold text-brand-textMain">{{ title }}</h3>
          <button @click="$emit('close')" class="w-8 h-8 rounded-full bg-brand-background flex items-center justify-center text-brand-textMuted">
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="p-6 pt-4 overflow-y-auto hide-scrollbar">
          <slot></slot>
        </div>

      </div>
    </transition>
  </Teleport>
</template>