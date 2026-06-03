<template>
  <div class="page">
    <h1>Conversations</h1>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-if="!loading" class="conversations-layout">
      <!-- Sidebar: Conversation List -->
      <div class="conversation-list">
        <button class="btn btn-full" @click="showCreatePanel = true">+ New Conversation</button>

        <div v-if="conversations.length === 0" class="empty">No conversations yet.</div>

        <div
          v-for="convo in conversations"
          :key="convo.id"
          class="conversation-item"
          :class="{ active: currentConversation?.id === convo.id }"
          @click="selectConversation(convo)"
        >
          <div class="convo-title">{{ convo.title }}</div>
          <div class="convo-meta">Doc #{{ convo.document_id }} | {{ formatDate(convo.created_at) }}</div>
        </div>
      </div>

      <!-- Messages Panel -->
      <div class="messages-panel">
        <!-- Create Form -->
        <div v-if="showCreatePanel" class="create-panel">
          <h3>New Conversation</h3>
          <form @submit.prevent="handleCreate">
            <div class="form-group">
              <label>Document ID</label>
              <input v-model.number="createForm.document_id" type="number" required />
            </div>
            <div class="form-group">
              <label>Title (optional)</label>
              <input v-model="createForm.title" type="text" placeholder="New Conversation" />
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="showCreatePanel = false">Cancel</button>
              <button type="submit" class="btn">Create</button>
            </div>
          </form>
        </div>

        <!-- Message List -->
        <div v-else-if="!currentConversation" class="empty-panel">
          Select a conversation to view messages.
        </div>

        <template v-else>
          <div class="messages-header">
            <h3>{{ currentConversation.title }}</h3>
          </div>

          <div v-if="messagesLoading" class="loading">Loading messages...</div>

          <div v-else class="messages-list">
            <div v-if="messages.length === 0" class="empty">No messages yet.</div>

            <div
              v-for="msg in messages"
              :key="msg.id"
              class="message"
              :class="msg.role"
            >
              <div class="message-role">{{ msg.role === 'user' ? 'You' : 'Assistant' }}</div>
              <div class="message-content">{{ msg.content }}</div>
              <div class="message-time">{{ formatDate(msg.created_at) }}</div>
            </div>
          </div>

          <!-- New Message Form -->
          <form class="message-form" @submit.prevent="handleSendMessage">
            <input
              v-model="newMessage"
              type="text"
              placeholder="Type a message..."
              required
            />
            <button type="submit" class="btn">Send</button>
          </form>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import type { Conversation, ConversationCreate } from '@/types/conversation'

const store = useStore()

const conversations = computed(() => store.state.conversations.conversations)
const currentConversation = computed(() => store.state.conversations.currentConversation)
const messages = computed(() => store.state.conversations.messages)
const loading = computed(() => store.state.conversations.loading)
const messagesLoading = computed(() => store.state.conversations.messagesLoading)
const error = computed(() => store.state.conversations.error)

const showCreatePanel = ref(false)
const newMessage = ref('')

const createForm = reactive<ConversationCreate>({
  document_id: 0,
  title: 'New Conversation',
})

onMounted(() => {
  store.dispatch('conversations/fetchConversations')
})

function selectConversation(convo: Conversation) {
  store.dispatch('conversations/fetchConversation', convo.id)
  store.dispatch('conversations/fetchMessages', convo.id)
}

function handleCreate() {
  store.dispatch('conversations/createConversation', { ...createForm })
  showCreatePanel.value = false
  createForm.document_id = 0
  createForm.title = 'New Conversation'
}

function handleSendMessage() {
  if (!currentConversation.value || !newMessage.value.trim()) return
  store.dispatch('conversations/createMessage', {
    conversation_id: currentConversation.value.id,
    role: 'user',
    content: newMessage.value,
  })
  newMessage.value = ''
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString()
}
</script>

<style scoped>
.page {
  max-width: 1200px;
}
h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 24px;
}
.loading,
.error {
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}
.loading {
  color: #64748b;
}
.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.conversations-layout {
  display: flex;
  gap: 24px;
  min-height: 500px;
}

/* Left Panel */
.conversation-list {
  width: 300px;
  min-width: 300px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 70vh;
  overflow-y: auto;
}

.conversation-item {
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.1s;
  border: 1px solid transparent;
}
.conversation-item:hover {
  background: #f8fafc;
}
.conversation-item.active {
  background: #eff6ff;
  border-color: #3b82f6;
}
.convo-title {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9rem;
}
.convo-meta {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 2px;
}

/* Right Panel */
.messages-panel {
  flex: 1;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  min-height: 500px;
}

.empty-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: #94a3b8;
  font-size: 0.9rem;
}

.messages-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
}
.messages-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #1e293b;
}

.messages-list {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
}
.message.user {
  align-self: flex-end;
  background: #3b82f6;
  color: #ffffff;
}
.message.assistant {
  align-self: flex-start;
  background: #f1f5f9;
  color: #1e293b;
}

.message-role {
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 4px;
  opacity: 0.8;
}
.message-content {
  font-size: 0.9rem;
  line-height: 1.5;
}
.message-time {
  font-size: 0.7rem;
  margin-top: 6px;
  opacity: 0.6;
}

.message-form {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  border-top: 1px solid #e2e8f0;
}
.message-form input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1e293b;
}
.message-form input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Create Panel */
.create-panel {
  padding: 24px;
}
.create-panel h3 {
  margin: 0 0 16px;
  color: #1e293b;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 500;
  color: #475569;
  margin-bottom: 4px;
}
.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #1e293b;
  box-sizing: border-box;
}
.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  background-color: #3b82f6;
  color: #ffffff;
  transition: background-color 0.15s;
}
.btn:hover {
  background-color: #2563eb;
}
.btn-secondary {
  background-color: #e2e8f0;
  color: #475569;
}
.btn-secondary:hover {
  background-color: #cbd5e1;
}
.btn-full {
  width: 100%;
  margin-bottom: 8px;
}
.empty {
  text-align: center;
  color: #94a3b8;
  padding: 24px;
  font-size: 0.9rem;
}
</style>
