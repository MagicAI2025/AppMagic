import React, { useState } from 'react'
import { Layout } from '@/components/Layout'
import { ProjectGenerator } from '@/components/ProjectGenerator'
import { ProjectList } from '@/components/ProjectList'
import { toast } from 'react-hot-toast'
import { generateProject } from '@/utils/api'
import { useRouter } from 'next/router'
import Features from '../components/Features'
import { useAuthStore } from '@/stores/auth'

export default function Home() {
  const [isGenerating, setIsGenerating] = useState(false)
  const router = useRouter()
  
  const handleGenerate = async (requirements: string) => {
    if (!useAuthStore.getState().token) {
      router.push(`/auth/login?redirect=${encodeURIComponent(router.asPath)}`)
      return
    }
    
    try {
      setIsGenerating(true)
      const result = await generateProject(requirements)
      router.push(`/projects/${result.project.id}`)
    } catch (error) {
      toast.error('生成失败，请登录后重试')
    } finally {
      setIsGenerating(false)
    }
  }
  
  return (
    <Layout>
      <div className="py-12">
        <div className="space-y-8">
          <header className="py-20 text-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
            <h1 className="text-5xl font-bold mb-4">
              App Magic AI
            </h1>
            <p className="text-xl mb-8">
              Create complete applications using natural language descriptions, just like magic.
            </p>
            <button 
              className="bg-white text-primary-600 font-bold py-4 px-8 rounded-full shadow-lg hover:shadow-xl transition duration-200 text-lg"
              onClick={() => router.push('/auth/register')}
            >
              Get Started
            </button>
          </header>
          
          <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold mb-4 text-center">
              Why App Magic AI?  
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white p-6 shadow rounded-lg">
                <h3 className="text-xl font-semibold mb-2">
                  🚀 Rapid Development
                </h3>
                <p className="text-gray-600">
                  Generate complete applications in minutes, not months. Get your ideas to market faster than ever before.
                </p>
              </div>
              <div className="bg-white p-6 shadow rounded-lg">
                <h3 className="text-xl font-semibold mb-2">
                  🧠 AI-Powered
                </h3>
                <p className="text-gray-600">
                  Leverage the power of artificial intelligence to automatically generate optimized and bug-free code.
                </p>
              </div>
              <div className="bg-white p-6 shadow rounded-lg">
                <h3 className="text-xl font-semibold mb-2">
                  🌍 Build Once, Deploy Anywhere
                </h3>
                <p className="text-gray-600">
                  Create applications that seamlessly run on web, mobile, and desktop with a single codebase.
                </p>
              </div>
            </div>
          </section>
          
          <Features />
          
          <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold mb-8 text-center">
              Recent Projects
            </h2>
            <ProjectList />
          </section>
        </div>
      </div>
    </Layout>
  )
} 