<!-- src/App.vue -->
<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { initGlobalTheme } from '@/config/ringThemeMap'

onMounted(() => {
  initGlobalTheme()
})
</script>

