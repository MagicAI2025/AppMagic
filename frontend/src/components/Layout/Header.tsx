import { Fragment } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { Menu, Transition } from '@headlessui/react'
import { useAuthStore } from '@/store/useAuthStore'

export function Header() {
  const router = useRouter()
  const user = useAuthStore(state => state.token)

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex justify-between h-16">
          <Link href="/" className="flex items-center">
            <span className="text-xl font-bold text-gray-900">
              App Magic AI
            </span>
          </Link>
          <div className="flex items-center space-x-6">
            <Link href="/docs" className="text-gray-700 hover:text-gray-900">
              Documentation
            </Link>
            <button
              onClick={() => {
                if (!user) {
                  router.push('/auth/login?redirect=/generate')
                } else {
                  router.push('/generate')
                }
              }}
              className="btn-primary px-6 py-2"
            >
              生成新应用
            </button>
          </div>
        </div>
      </div>
    </header>
  )
} 