import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuthStore } from '@/store/useAuthStore'
import { LoadingSpinner } from '../LoadingSpinner'

interface Props {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: Props) {
  const router = useRouter()
  const { token, loading } = useAuthStore()

  useEffect(() => {
    if (!loading && !token) {
      router.push('/auth/login')
    }
  }, [loading, token, router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (!token) {
    return null
  }

  return <>{children}</>
} 