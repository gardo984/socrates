import { createStore } from 'vuex'
import authModule, { type AuthState } from './modules/auth'
import usersModule, { type UsersState } from './modules/users'
import documentsModule, { type DocumentsState } from './modules/documents'
import conversationsModule, { type ConversationsState } from './modules/conversations'

export interface RootState {
  sidebarCollapsed: boolean
  auth: AuthState
  users: UsersState
  documents: DocumentsState
  conversations: ConversationsState
}

const store = createStore<RootState>({
  state: {
    sidebarCollapsed: false,
  } as RootState,
  mutations: {
    TOGGLE_SIDEBAR(state) {
      state.sidebarCollapsed = !state.sidebarCollapsed
    },
  },
  modules: {
    auth: authModule,
    users: usersModule,
    documents: documentsModule,
    conversations: conversationsModule,
  },
})

export default store
