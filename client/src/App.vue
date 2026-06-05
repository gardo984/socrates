<template>
  <AppLayout v-if="!isAuthPage && isAuthenticated" />
  <router-view v-else-if="isAuthPage || !isAuthenticated" />
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import AppLayout from '@/components/AppLayout.vue'

const route = useRoute()
const router = useRouter()
const store = useStore()

const authPageNames = ['login', 'forgot-password']
const isAuthPage = computed(() => authPageNames.includes(route.name as string))
const isAuthenticated = computed(() => {
  return !!(store.state.auth.token && store.state.auth.currentUser)
})

onMounted(async () => {
  const token = store.state.auth.token
  const hasUser = !!store.state.auth.currentUser

  if (token && !hasUser) {
    await store.dispatch('auth/fetchCurrentUser')
  }

  if (!store.state.auth.token) {
    router.push('/login')
  }
})
</script>
