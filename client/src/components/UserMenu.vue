<template>
  <div class="user-menu" ref="menuRef">
    <button class="user-trigger" @click.stop="open = !open" :title="currentUser?.name ?? 'User menu'">
      <span class="user-avatar">{{ initials }}</span>
    </button>
    <Transition name="dropdown">
      <div v-if="open" class="dropdown-panel">
        <div class="dropdown-user-info">
          <span class="dropdown-user-name">{{ currentUser?.name ?? 'User' }}</span>
          <span class="dropdown-user-email">{{ currentUser?.email ?? '' }}</span>
        </div>
        <hr class="dropdown-divider" />
        <router-link to="/user-info" class="dropdown-item" @click="open = false">
          <svg class="dropdown-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
          </svg>
          User Information
        </router-link>
        <router-link to="/reset-password" class="dropdown-item" @click="open = false">
          <svg class="dropdown-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
          </svg>
          Reset Password
        </router-link>
        <hr class="dropdown-divider" />
        <button class="dropdown-item dropdown-item--danger" @click="handleLogout">
          <svg class="dropdown-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
          </svg>
          Log Out
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const open = ref(false)
const menuRef = ref<HTMLElement | null>(null)

const currentUser = computed(() => store.state.auth.currentUser)

const initials = computed(() => {
  const name = currentUser.value?.name ?? '?'
  const parts = name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

function handleLogout() {
  open.value = false
  store.dispatch('auth/logout')
}

function onClickOutside(e: MouseEvent) {
  if (menuRef.value && !menuRef.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', onClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', onClickOutside)
})
</script>

<style scoped>
.user-menu {
  position: relative;
}

.user-trigger {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  border-radius: 50%;
  transition: opacity 0.15s;
}

.user-trigger:hover {
  opacity: 0.8;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #3b82f6;
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 600;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 220px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-user-info {
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dropdown-user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.dropdown-user-email {
  font-size: 0.8rem;
  color: #64748b;
}

.dropdown-divider {
  margin: 0;
  border: none;
  border-top: 1px solid #e2e8f0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  font-size: 0.875rem;
  color: #334155;
  text-decoration: none;
  cursor: pointer;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  transition: background-color 0.12s;
}

.dropdown-item:hover {
  background-color: #f1f5f9;
}

.dropdown-item--danger {
  color: #ef4444;
}

.dropdown-item--danger:hover {
  background-color: #fef2f2;
}

.dropdown-icon {
  flex-shrink: 0;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.12s ease, transform 0.12s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
