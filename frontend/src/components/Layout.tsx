import React from 'react'
import { Fragment } from 'react'
import Head from 'next/head'
import { Menu, Transition } from '@headlessui/react'
import { useAuthStore } from '@/store/useAuthStore'
import { useRouter } from 'next/router'
import Logo from './Logo'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const router = useRouter()
  const { user, logout } = useAuthStore()
  
  const handleLogout = () => {
    logout()
    router.push('/auth/login')
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>AI 应用生成平台</title>
        <meta name="description" content="使用 AI 快速生成完整应用" />
      </Head>
      
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Logo />
            </div>
            
            <div className="flex items-center">
              {user && (
                <Menu as="div" className="ml-3 relative">
                  <Menu.Button className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                    <span className="sr-only">打开用户菜单</span>
                    <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                      <span className="text-primary-700 font-medium">
                        {user.username[0].toUpperCase()}
                      </span>
                    </div>
                  </Menu.Button>
                  
                  <Transition
                    as={Fragment}
                    enter="transition ease-out duration-100"
                    enterFrom="transform opacity-0 scale-95"
                    enterTo="transform opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leaveFrom="transform opacity-100 scale-100"
                    leaveTo="transform opacity-0 scale-95"
                  >
                    <Menu.Items className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                      <div className="py-1">
                        <Menu.Item>
                          {({ active }) => (
                            <button
                              onClick={handleLogout}
                              className={`${
                                active ? 'bg-gray-100' : ''
                              } block w-full text-left px-4 py-2 text-sm text-gray-700`}
                            >
                              退出登录
                            </button>
                          )}
                        </Menu.Item>
                      </div>
                    </Menu.Items>
                  </Transition>
                </Menu>
              )}
            </div>
          </div>
        </div>
      </nav>
      
      <main>{children}</main>
    </div>
  )
} 