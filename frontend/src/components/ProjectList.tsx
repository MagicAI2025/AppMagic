import { useEffect, useState } from 'react'
import { listProjects } from '@/utils/api'
import Link from 'next/link'

interface Project {
  id: number
  description: string
  project_type: string
  created_at: string
}

export function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const data = await listProjects()
        setProjects(data.projects)
      } catch (error) {
        console.error('Failed to fetch projects:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchProjects()
  }, [])
  
  if (loading) {
    return <div>Loading...</div>
  }
  
  return (
    <div className="bg-white shadow rounded-lg">
      <ul className="divide-y divide-gray-200">
        {projects.map((project) => (
          <li key={project.id} className="p-4 hover:bg-gray-50">
            <Link href={`/projects/${project.id}`}>
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {project.description}
                  </h3>
                  <p className="text-sm text-gray-500">
                    Type: {project.project_type}
                  </p>
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