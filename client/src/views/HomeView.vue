<template>
  <div class="page">
    <h1>Dashboard</h1>
    <p>Welcome to the Socrates project management interface.</p>

    <div class="cards">
      <div class="card" @click="$router.push('/users')">
        <div class="card-icon">&#x1F465;</div>
        <div class="card-body">
          <h3>Users</h3>
          <p>{{ userCount }} registered users</p>
        </div>
      </div>
      <div class="card" @click="$router.push('/documents')">
        <div class="card-icon">&#x1F4C4;</div>
        <div class="card-body">
          <h3>Documents</h3>
          <p>{{ docCount }} uploaded documents</p>
        </div>
      </div>
      <div class="card" @click="$router.push('/conversations')">
        <div class="card-icon">&#x1F4AC;</div>
        <div class="card-body">
          <h3>Conversations</h3>
          <p>{{ convoCount }} conversations</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const userCount = computed(() => store.state.users.users.length)
const docCount = computed(() => store.state.documents.documents.length)
const convoCount = computed(() => store.state.conversations.conversations.length)

onMounted(() => {
  store.dispatch('users/fetchUsers')
  store.dispatch('documents/fetchDocuments')
  store.dispatch('conversations/fetchConversations')
})
</script>

<style scoped>
.page {
  max-width: 720px;
}

h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 32px;
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 24px;
  cursor: pointer;
  transition: box-shadow 0.15s, border-color 0.15s;
}

.card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border-color: #3b82f6;
}

.card-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 10px;
}

.card-body h3 {
  margin: 0 0 4px;
  font-size: 1.05rem;
  color: #1e293b;
}

.card-body p {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
}
</style>
