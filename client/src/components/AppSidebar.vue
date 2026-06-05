<template>
  <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
    <div class="sidebar-header">
      <h2 v-if="!sidebarCollapsed">Socrates</h2>
      <h2 v-else class="sidebar-logo-collapsed">S</h2>
      <button class="toggle-btn" @click="toggleSidebar" :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'">
        <span v-if="sidebarCollapsed" class="toggle-icon">&#x276F;</span>
        <span v-else class="toggle-icon">&#x276E;</span>
      </button>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item" exact-active-class="active">
        <span class="nav-icon">&#x1F3E0;</span>
        <span v-if="!sidebarCollapsed" class="nav-label">Dashboard</span>
      </router-link>
      <router-link to="/users" class="nav-item" active-class="active">
        <span class="nav-icon">&#x1F465;</span>
        <span v-if="!sidebarCollapsed" class="nav-label">Users</span>
      </router-link>
      <router-link to="/documents" class="nav-item" active-class="active">
        <span class="nav-icon">&#x1F4C4;</span>
        <span v-if="!sidebarCollapsed" class="nav-label">Documents</span>
      </router-link>
      <router-link to="/conversations" class="nav-item" active-class="active">
        <span class="nav-icon">&#x1F4AC;</span>
        <span v-if="!sidebarCollapsed" class="nav-label">Conversations</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const sidebarCollapsed = computed(() => store.state.sidebarCollapsed)

function toggleSidebar() {
  store.commit('TOGGLE_SIDEBAR')
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  min-width: 240px;
  height: 100vh;
  background-color: #1e293b;
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  transition: width 0.2s ease, min-width 0.2s ease;
}

.sidebar.collapsed {
  width: 64px;
  min-width: 64px;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid #334155;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.sidebar.collapsed .sidebar-header {
  justify-content: center;
  padding: 24px 8px;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: 0.025em;
  white-space: nowrap;
}

.sidebar-logo-collapsed {
  font-size: 1.5rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: color 0.15s, background-color 0.15s;
  flex-shrink: 0;
}

.toggle-btn:hover {
  color: #e2e8f0;
  background-color: #334155;
}

.sidebar.collapsed .toggle-btn {
  margin-top: 0;
}

.toggle-icon {
  font-size: 0.9rem;
  line-height: 1;
}

.sidebar-nav {
  padding: 12px 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.15s, color 0.15s;
  margin: 0 8px;
  border-radius: 6px;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px 8px;
  margin: 0 4px;
}

.nav-item:hover {
  background-color: #334155;
  color: #e2e8f0;
}

.nav-item.active {
  background-color: #3b82f6;
  color: #ffffff;
}

.nav-icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.nav-label {
  line-height: 1;
}
</style>
