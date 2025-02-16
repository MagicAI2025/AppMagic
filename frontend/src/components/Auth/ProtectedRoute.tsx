import React from 'react'
import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuthStore } from '@/store/useAuthStore'
import { LoadingSpinner } from '../LoadingSpinner'

interface Props {
  children: React.ReactNode
  publicRoutes?: string[]
}

export function ProtectedRoute({ children, publicRoutes = [] }: Props) {
  const router = useRouter()
  const { token, loading } = useAuthStore()

  const pathIsPublic = publicRoutes.some(path => 
    router.pathname === path || router.pathname.startsWith(`${path}/`)
  )

  useEffect(() => {
    if (!loading && !token && !pathIsPublic) {
      router.push(`/auth/login?redirect=${encodeURIComponent(router.asPath)}`)
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