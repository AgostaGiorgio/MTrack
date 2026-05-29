<script setup>
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { Home, List, Settings } from 'lucide-vue-next'
import AppHeader from './components/AppHeader.vue'

const route = useRoute()
</script>

<template>
  <div class="min-h-screen bg-brand-background text-brand-textMain font-sans pb-24 selection:bg-brand-primary selection:text-white">
    
    <AppHeader />

    <main class="px-4">
      <RouterView />
    </main>

    <nav class="fixed bottom-6 left-6 right-6 bg-brand-surface/70 backdrop-blur-xl border border-white/10 shadow-app rounded-[24px] z-50">
      <div class="flex justify-around items-center p-4">
        <RouterLink to="/" class="flex flex-col items-center gap-1 transition-colors duration-200" :class="route.path === '/' ? 'text-brand-primary' : 'text-brand-textMuted'">
          <Home :size="20" :stroke-width="route.path === '/' ? 2.5 : 2" />
        </RouterLink>

        <RouterLink to="/transactions" class="flex flex-col items-center gap-1 transition-colors duration-200" :class="route.path === '/transactions' ? 'text-brand-primary' : 'text-brand-textMuted'">
          <List :size="20" :stroke-width="route.path === '/transactions' ? 2.5 : 2" />
        </RouterLink>

        <RouterLink to="/categories" class="flex flex-col items-center gap-1 transition-colors duration-200" :class="route.path === '/categories' ? 'text-brand-primary' : 'text-brand-textMuted'">
          <Settings :size="20" :stroke-width="route.path === '/categories' ? 2.5 : 2" />
        </RouterLink>
      </div>
    </nav>
  </div>
</template>