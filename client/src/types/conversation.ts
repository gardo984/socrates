export interface Conversation {
  id: number
  document_id: number
  title: string
  created_at: string
  updated_at: string
}

export interface ConversationCreate {
  document_id: number
  title?: string
}

export interface ConversationUpdate {
  title?: string
}

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
  metadata: Record<string, unknown> | null
}

export interface MessageCreate {
  conversation_id: number
  role: 'user' | 'assistant'
  content: string
  metadata_?: Record<string, unknown>
}
