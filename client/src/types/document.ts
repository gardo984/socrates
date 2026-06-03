export interface Document {
  id: number
  filename: string
  file_type: string | null
  file_size: number | null
  uploaded_at: string
  user_id: number | null
}
