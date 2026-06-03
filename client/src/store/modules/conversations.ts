import type { Module, ActionContext } from 'vuex'
import type { RootState } from '@/store'
import type { Conversation, ConversationCreate, Message, MessageCreate } from '@/types/conversation'
import apiClient from '@/api/client'

export interface ConversationsState {
  conversations: Conversation[]
  currentConversation: Conversation | null
  messages: Message[]
  loading: boolean
  messagesLoading: boolean
  error: string | null
}

type ConvoCtx = ActionContext<ConversationsState, RootState>

const conversationsModule: Module<ConversationsState, RootState> = {
  namespaced: true,
  state: (): ConversationsState => ({
    conversations: [],
    currentConversation: null,
    messages: [],
    loading: false,
    messagesLoading: false,
    error: null,
  }),
  mutations: {
    SET_LOADING(state: ConversationsState, value: boolean) {
      state.loading = value
    },
    SET_MESSAGES_LOADING(state: ConversationsState, value: boolean) {
      state.messagesLoading = value
    },
    SET_ERROR(state: ConversationsState, value: string | null) {
      state.error = value
    },
    SET_CONVERSATIONS(state: ConversationsState, convos: Conversation[]) {
      state.conversations = convos
    },
    ADD_CONVERSATION(state: ConversationsState, convo: Conversation) {
      state.conversations.unshift(convo)
    },
    SET_CURRENT_CONVERSATION(state: ConversationsState, convo: Conversation | null) {
      state.currentConversation = convo
    },
    SET_MESSAGES(state: ConversationsState, msgs: Message[]) {
      state.messages = msgs
    },
    ADD_MESSAGE(state: ConversationsState, msg: Message) {
      state.messages.push(msg)
    },
  },
  actions: {
    async fetchConversations({ commit }: ConvoCtx) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.get<Conversation[]>('/conversations/')
        commit('SET_CONVERSATIONS', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to fetch conversations'
        commit('SET_ERROR', msg)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchConversation({ commit }: ConvoCtx, conversationId: number) {
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.get<Conversation>(`/conversations/${conversationId}`)
        commit('SET_CURRENT_CONVERSATION', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to fetch conversation'
        commit('SET_ERROR', msg)
      }
    },
    async createConversation({ commit }: ConvoCtx, data: ConversationCreate) {
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.post<Conversation>('/conversations/', data)
        commit('ADD_CONVERSATION', res.data)
        commit('SET_CURRENT_CONVERSATION', res.data)
        commit('SET_MESSAGES', [])
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to create conversation'
        commit('SET_ERROR', msg)
      }
    },
    async fetchMessages({ commit }: ConvoCtx, conversationId: number) {
      commit('SET_MESSAGES_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.get<Message[]>(`/conversations/${conversationId}/messages`)
        commit('SET_MESSAGES', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to fetch messages'
        commit('SET_ERROR', msg)
      } finally {
        commit('SET_MESSAGES_LOADING', false)
      }
    },
    async createMessage({ commit }: ConvoCtx, data: MessageCreate) {
      commit('SET_ERROR', null)
      try {
        const res = await apiClient.post<Message>(
          `/conversations/${data.conversation_id}/messages`,
          data,
        )
        commit('ADD_MESSAGE', res.data)
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : 'Failed to create message'
        commit('SET_ERROR', msg)
      }
    },
  },
}

export default conversationsModule
