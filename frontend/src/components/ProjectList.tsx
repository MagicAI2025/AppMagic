import React from 'react'
import { useEffect, useState } from 'react'
import { listProjects } from '@/utils/api'
import Link from 'next/link'
import { LoadingSpinner } from '@/components/LoadingSpinner'
import { ProjectIcon } from '@/components/ProjectIcon'

interface Project {
  id: number
  description: string
  project_type: string
  created_at: string
}

export function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([])
  
  useEffect(() => {
    const fetchProjects = async () => {
      const data = await listProjects()
      setProjects(data)
    }
    fetchProjects()
  }, [])
  
  if (projects.length === 0) {
    return <div>Loading...</div>
  }
  
  return (
    <div className="bg-white shadow rounded-lg">
      <ul className="divide-y divide-gray-200">
        {projects.map((project) => (
          <li key={project.id} className="p-4 hover:bg-gray-50">
            <Link href={`/projects/${project.id}`}>
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <span className="inline-flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                      <ProjectIcon className="h-6 w-6" />
                    </span>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">
                      {project.description}
                    </h3>
                    <p className="text-sm text-gray-500">
                      Type: {project.project_type}
                    </p>
                    <div className="mt-2 flex space-x-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Active
                      </span>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        Web
                      </span>
                    </div>
                  </div>
                </div>
                <span className="text-sm text-gray-500">
                  {new Date(project.created_at).toLocaleDateString()}
                </span>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
} 