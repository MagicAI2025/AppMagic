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
  loading: boolean
  setToken: (token: string | null) => void
  setUser: (user: User | null) => void
  logout: () => void
  initializeAuth: () => Promise<void>
}

const STORAGE_KEY = 'auth-storage'

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      loading: true,
      setToken: (token) => {
        set({ token })
        if (token) {
          localStorage.setItem('auth-token', token)
        } else {
          localStorage.removeItem('auth-token')
        }
      },
      setUser: (user) => set({ user }),
      logout: () => {
        set({ token: null, user: null })
        localStorage.removeItem('auth-token')
      },
      initializeAuth: async () => {
        try {
          const token = localStorage.getItem('auth-token')
          if (token) {
            set({ token }) // Set token to state
            const response = await api.get('/api/users/me')
            set({ user: response.data, loading: false })
          } else {
            set({ loading: false })
          }
        } catch (error) {
          set({ token: null, user: null, loading: false })
        }
      }
    }),
    {
      name: STORAGE_KEY,
      getStorage: () => localStorage
    }
  )
) 