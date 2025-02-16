import React, { useEffect } from 'react'
import { useAuthStore } from '../store/useAuthStore'
import { useRouter } from 'next/router'
import Layout from '../components/Layout/Layout'
import ProjectGenerator from '../components/ProjectGenerator/ProjectGenerator'

export default function GeneratePage() {
  const { token } = useAuthStore()
  const router = useRouter()

  useEffect(() => {
    if (!token) {
      router.push('/auth/login?redirect=/generate')
    }
  }, [token])

  return (
    <Layout>
      <ProjectGenerator 
        onGenerate={handleGenerate}
        isGenerating={isGenerating}
      />
    </Layout>
  )
} 