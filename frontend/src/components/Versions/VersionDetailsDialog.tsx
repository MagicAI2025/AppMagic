import React from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { Fragment } from 'react'
import { DiffEditor } from '@monaco-editor/react'

interface VersionFile {
  path: string
  content: string
  type: string
  changes: {
    added: number
    removed: number
    modified: number
  }
}

interface VersionDetails {
  id: number
  version_number: string
  description: string
  created_by: {
    id: number
    username: string
  }
  created_at: string
  files: VersionFile[]
}

interface Props {
  isOpen: boolean
  onClose: () => void
  version: VersionDetails | null
}

export function VersionDetailsDialog({ isOpen, onClose, version }: Props) {
  if (!version) return null

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-4xl transform overflow-hidden rounded-2xl bg-white p-6 shadow-xl transition-all">
                <Dialog.Title
                  as="h3"
                  className="text-lg font-medium leading-6 text-gray-900 mb-4"
                >
                  Version {version.version_number} Details
                </Dialog.Title>

                <div className="mt-2 space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-gray-700">Description</h4>
                    <p className="mt-1 text-sm text-gray-600">
                      {version.description}
                    </p>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium text-gray-700">Created By</h4>
                    <p className="mt-1 text-sm text-gray-600">
                      {version.created_by.username} at{' '}
                      {new Date(version.created_at).toLocaleString()}
                    </p>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-2">
                      Changed Files
                    </h4>
                    <div className="space-y-4">
                      {version.files.map((file) => (
                        <div
                          key={file.path}
                          className="border border-gray-200 rounded-lg overflow-hidden"
                        >
                          <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
                            <div className="flex items-center justify-between">
                              <span className="font-medium text-sm">
                                {file.path}
                              </span>
                              <div className="text-xs text-gray-500 space-x-2">
                                <span className="text-green-600">
                                  +{file.changes.added}
                                </span>
                                <span className="text-red-600">
                                  -{file.changes.removed}
                                </span>
                                <span className="text-blue-600">
                                  ~{file.changes.modified}
                                </span>
                              </div>
                            </div>
                          </div>
                          <div className="max-h-96 overflow-auto">
                            <DiffEditor
                              original={previousVersionContent}
                              modified={file.content}
                              language={file.type}
                              options={{ readOnly: true }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <button
                    type="button"
                    className="btn-primary w-full"
                    onClick={onClose}
                  >
                    Close
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  )
} 