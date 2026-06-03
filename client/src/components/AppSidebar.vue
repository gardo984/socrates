<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>Socrates</h2>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item" exact-active-class="active">
        <span class="nav-icon">&#x1F3E0;</span>
        <span class="nav-label">Home</span>
      </router-link>
      <router-link to="/about" class="nav-item" active-class="active">
        <span class="nav-icon">&#x2139;&#xFE0F;</span>
        <span class="nav-label">About</span>
      </router-link>
      <router-link to="/contact" class="nav-item" active-class="active">
        <span class="nav-icon">&#x2709;&#xFE0F;</span>
        <span class="nav-label">Contact</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
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
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid #334155;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: 0.025em;
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
  border-radius: 0;
  margin: 0 8px;
  border-radius: 6px;
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
