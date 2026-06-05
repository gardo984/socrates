<template>
  <div class="layout">
    <AppSidebar />
    <div class="content-area" :style="{ marginLeft: sidebarCollapsed ? '64px' : '240px' }">
      <header class="top-bar">
        <div class="top-bar-left"></div>
        <div class="top-bar-right">
          <router-link v-if="!currentUser" to="/login" class="login-link">Sign In</router-link>
          <UserMenu v-else />
        </div>
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'
import AppSidebar from './AppSidebar.vue'
import UserMenu from './UserMenu.vue'

const store = useStore()
const sidebarCollapsed = computed(() => store.state.sidebarCollapsed)
const currentUser = computed(() => store.state.auth.currentUser)
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left 0.2s ease;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 32px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.top-bar-right {
  display: flex;
  align-items: center;
}

.login-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: #3b82f6;
  text-decoration: none;
  padding: 6px 14px;
  border: 1px solid #3b82f6;
  border-radius: 6px;
  transition: background-color 0.15s, color 0.15s;
}

.login-link:hover {
  background-color: #3b82f6;
  color: #ffffff;
}

.main-content {
  flex: 1;
  padding: 32px;
  background-color: #f8fafc;
}
</style>
