import { useAuthStore } from '@/store/useAuthStore'

export const getAuthHeaders = () => {
  const token = useAuthStore.getState().token
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export const isAuthenticated = () => {
  return !!useAuthStore.getState().token
} 