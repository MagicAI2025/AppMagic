import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { Layout } from '@/components/Layout'
import { CodeEditor } from '@/components/CodeEditor'
import { ProjectComments } from '@/components/ProjectComments'
import { ProjectVersions } from '@/components/ProjectVersions'
import { getProject } from '@/utils/api'
import { toast } from 'react-hot-toast'
import { Tab } from '@headlessui/react'
import api from '@/utils/api'

interface ProjectFile {
  path: string
  content: string
  type: string
}

interface Project {
  id: number
  description: string
  project_type: string
  structure: any
  created_at: string
  files: ProjectFile[]
}

export default function ProjectDetail() {
  const router = useRouter()
  const { id } = router.query
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedFile, setSelectedFile] = useState<ProjectFile | null>(null)
  const [saving, setSaving] = useState(false)
  
  useEffect(() => {
    if (id) {
      fetchProject()
    }
  }, [id])
  
  const fetchProject = async () => {
    try {
      setLoading(true)
      const data = await getProject(id as string)
      setProject(data.project)
      if (data.project.files.length > 0) {
        setSelectedFile(data.project.files[0])
      }
    } catch (error) {
      toast.error('Failed to load project')
    } finally {
      setLoading(false)
    }
  }
  
  const handleCodeChange = async (newContent: string) => {
    if (!selectedFile) return

    try {
      setSaving(true)
      await api.patch(`/api/projects/${project?.id}/files`, {
        path: selectedFile.path,
        content: newContent
      })
      
      // 更新本地状态
      setProject((prev) => {
        if (!prev) return prev
        return {
          ...prev,
          files: prev.files.map((file) => 
            file.path === selectedFile.path 
              ? { ...file, content: newContent }
              : file
          )
        }
      })
      
      setSelectedFile((prev) => 
        prev ? { ...prev, content: newContent } : prev
      )
      
      toast.success('File saved successfully')
    } catch (error) {
      toast.error('Failed to save file')
    } finally {
      setSaving(false)
    }
  }
  
  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          Loading...
        </div>
      </Layout>
    )
  }
  
  if (!project) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          Project not found
        </div>
      </Layout>
    )
  }
  
  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {project.description}
          </h1>
          <div className="text-sm text-gray-500">
            Created at {new Date(project.created_at).toLocaleString()}
          </div>
        </div>
        
        <div className="grid grid-cols-12 gap-6">
          {/* File List */}
          <div className="col-span-3">
            <div className="bg-white shadow rounded-lg overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-200">
                <h3 className="text-lg font-medium">Project Files</h3>
              </div>
              <div className="divide-y divide-gray-200">
                {project.files.map((file) => (
                  <button
                    key={file.path}
                    className={`w-full px-4 py-3 text-left hover:bg-gray-50 focus:outline-none
                      ${selectedFile?.path === file.path ? 'bg-primary-50' : ''}`}
                    onClick={() => setSelectedFile(file)}
                  >
                    <div className="text-sm font-medium text-gray-900">
                      {file.path}
                    </div>
                    <div className="text-xs text-gray-500">
                      {file.type}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
          
          {/* Main Content Area */}
          <div className="col-span-9">
            <Tab.Group>
              <Tab.List className="flex space-x-1 rounded-xl bg-white p-1 shadow mb-4">
                <Tab
                  className={({ selected }) =>
                    `w-full rounded-lg py-2.5 text-sm font-medium leading-5
                     ${selected
                       ? 'bg-primary-100 text-primary-700'
                       : 'text-gray-700 hover:bg-gray-100'
                     }`
                  }
                >
                  Code
                </Tab>
                <Tab
                  className={({ selected }) =>
                    `w-full rounded-lg py-2.5 text-sm font-medium leading-5
                     ${selected
                       ? 'bg-primary-100 text-primary-700'
                       : 'text-gray-700 hover:bg-gray-100'
                     }`
                  }
                >
                  Comments
                </Tab>
                <Tab
                  className={({ selected }) =>
                    `w-full rounded-lg py-2.5 text-sm font-medium leading-5
                     ${selected
                       ? 'bg-primary-100 text-primary-700'
                       : 'text-gray-700 hover:bg-gray-100'
                     }`
                  }
                >
                  Versions
                </Tab>
              </Tab.List>
              
              <Tab.Panels>
                <Tab.Panel>
                  {selectedFile ? (
                    <div className="bg-white shadow rounded-lg overflow-hidden">
                      <CodeEditor
                        value={selectedFile.content}
                        language={selectedFile.type}
                        onChange={handleCodeChange}
                        readOnly={saving}
                      />
                    </div>
                  ) : (
                    <div className="bg-white shadow rounded-lg p-4">
                      Please select a file to view
                    </div>
                  )}
                </Tab.Panel>
                
                <Tab.Panel>
                  <ProjectComments projectId={project.id} />
                </Tab.Panel>
                
                <Tab.Panel>
                  <ProjectVersions projectId={project.id} />
                </Tab.Panel>
              </Tab.Panels>
            </Tab.Group>
          </div>
        </div>
      </div>
    </Layout>
  )
} 