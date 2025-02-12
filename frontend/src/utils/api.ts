import axios from 'axios'
import { useAuthStore } from '@/store/useAuthStore'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/auth/login'
    }
    if (error.response?.status === 403) {
      throw new Error('No permission to perform this operation')
    }
    return Promise.reject(error)
  }
)

export const generateProject = async (requirements: string) => {
  const response = await api.post('/api/generate', { description: requirements })
  return response.data
}

export const getProject = async (projectId: string) => {
  const response = await api.get(`/api/projects/${projectId}`)
  return response.data
}

export const listProjects = async (params?: {
  skip?: number
  limit?: number
  projectType?: string
}) => {
  const response = await api.get('/api/projects', { params })
  return response.data
}

export const login = async (email: string, password: string) => {
  const response = await api.post('/api/auth/token', {
    username: email,
    password
  })
  return response.data
}

export const register = async (data: {
  email: string
  username: string
  password: string
}) => {
  const response = await api.post('/api/auth/register', data)
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/api/users/me')
  return response.data
}

export default api 