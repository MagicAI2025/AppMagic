import create from 'zustand'
import { persist } from 'zustand/middleware'
import api from '@/utils/api'

interface User {
  id: number
  username: string
  email: string
}

interface AuthState {
  token: string | null
  user: User | null
  login: (token: string, user: User) => void
  logout: () => void
}

const STORAGE_KEY = 'auth-storage'

export const useAuthStore = create<AuthState>()(persist(
  (set) => ({
    token: null,
    user: null,
    login: (token, user) => set({ token, user }),
    logout: () => set({ token: null, user: null })
  }),
  { name: 'auth-store' }
)) 