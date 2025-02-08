import React, { useEffect } from 'react'
import type { AppProps } from 'next/app'
import { useRouter } from 'next/router'
import { Toaster } from 'react-hot-toast'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { ProtectedRoute } from '@/components/Auth/ProtectedRoute'
import { useAuthStore } from '@/store/useAuthStore'
import '@/styles/globals.css'

const publicPaths = ['/auth/login', '/auth/register']

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter()
  const { initializeAuth } = useAuthStore()

  useEffect(() => {
    initializeAuth()
  }, [initializeAuth])

  return (
    <ErrorBoundary>
      {publicPaths.includes(router.pathname) ? (
        <Component {...pageProps} />
      ) : (
        <ProtectedRoute>
          <Component {...pageProps} />
        </ProtectedRoute>
      )}
      <Toaster position="top-right" />
    </ErrorBoundary>
  )
} 