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

    <nav class="fixed bottom-0 left-0 w-full bg-brand-surface shadow-app rounded-t-app z-50">
      <div class="flex justify-around items-center p-4">
        
        <RouterLink to="/" class="flex flex-col items-center gap-1 transition-colors duration-200" :class="route.path === '/' ? 'text-brand-primary' : 'text-brand-textMuted'">
          <Home :size="24" :stroke-width="route.path === '/' ? 2.5 : 2" />
          <span class="text-[10px] font-semibold tracking-wide uppercase">Home</span>
        </RouterLink>

        <RouterLink to="/transactions" class="flex flex-col items-center gap-1 transition-colors duration-200" :class="route.path === '/transactions' ? 'text-brand-primary' : 'text-brand-textMuted'">
          <List :size="24" :stroke-width="route.path === '/transactions' ? 2.5 : 2" />
          <span class="text-[10px] font-semibold tracking-wide uppercase">Spese</span>
        </RouterLink>

        <RouterLink to="/categories" class="flex flex-col items-center gap-1 transition-colors duration-200" :class="route.path === '/categories' ? 'text-brand-primary' : 'text-brand-textMuted'">
          <Settings :size="24" :stroke-width="route.path === '/categories' ? 2.5 : 2" />
          <span class="text-[10px] font-semibold tracking-wide uppercase">Impostazioni</span>
        </RouterLink>

      </div>
    </nav>
  </div>
</template>