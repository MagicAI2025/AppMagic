import React, { useEffect } from 'react'
import type { AppProps } from 'next/app'
import { useRouter } from 'next/router'
import { Toaster } from 'react-hot-toast'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import '@/styles/globals.css'

const publicPaths = ['/auth/login', '/auth/register']

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter()

  // 添加SSR兼容处理
  if (typeof window === 'undefined') {
    useAuthStore.persist.rehydrate()
  }

  return (
    <ErrorBoundary>
      <Component {...pageProps} />
      <Toaster position="top-right" />
    </ErrorBoundary>
  )
} 