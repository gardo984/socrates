import { createStore } from 'vuex'
import usersModule, { type UsersState } from './modules/users'
import documentsModule, { type DocumentsState } from './modules/documents'
import conversationsModule, { type ConversationsState } from './modules/conversations'

export interface RootState {
  users: UsersState
  documents: DocumentsState
  conversations: ConversationsState
}

const store = createStore<RootState>({
  modules: {
    users: usersModule,
    documents: documentsModule,
    conversations: conversationsModule,
  },
})

export default store
