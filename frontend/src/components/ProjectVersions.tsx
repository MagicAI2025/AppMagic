import React, { useState, useEffect, useCallback } from 'react'
import api from '@/utils/api'
import { toast } from 'react-hot-toast'
import { VersionDetailsDialog } from './Versions/VersionDetailsDialog'
import type { VersionDetails } from './Versions/VersionDetailsDialog'

interface Version {
  id: number
  version_number: string
  description: string
  created_by: {
    id: number
    username: string
  }
  created_at: string
}

interface ProjectVersionsProps {
  projectId: number
}

interface CreateVersionData {
  description: string
}

export function ProjectVersions({ projectId }: ProjectVersionsProps) {
  const [versions, setVersions] = useState<Version[]>([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [newVersion, setNewVersion] = useState<CreateVersionData>({
    description: ''
  })
  const [selectedVersion, setSelectedVersion] = useState<VersionDetails | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  
  const fetchVersions = useCallback(async () => {
    try {
      const response = await api.get(`/api/projects/${projectId}/versions`)
      setVersions(response.data.versions)
    } catch (error) {
      toast.error('Failed to load version history')
    } finally {
      setLoading(false)
    }
  }, [projectId])
  
  useEffect(() => {
    fetchVersions()
  }, [fetchVersions])
  
  const handleCreateVersion = async () => {
    try {
      setCreating(true)
      await api.post(`/api/projects/${projectId}/versions`, newVersion)
      await fetchVersions()
      setNewVersion({ description: '' })
      toast.success('Version created successfully')
    } catch (error) {
      toast.error('Failed to create version')
    } finally {
      setCreating(false)
    }
  }

  const handleViewVersion = async (versionId: number) => {
    try {
      const response = await api.get(`/api/projects/${projectId}/versions/${versionId}`)
      setSelectedVersion(response.data.version)
      setDialogOpen(true)
    } catch (error) {
      toast.error('Failed to load version details')
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }
  
  return (
    <>
      <div className="space-y-6">
        {/* Create New Version */}
        <div className="bg-white shadow rounded-lg p-4">
          <h3 className="text-lg font-medium mb-4">Create New Version</h3>
          <div className="space-y-4">
            <textarea
              className="input-primary"
              rows={3}
              placeholder="Version description..."
              value={newVersion.description}
              onChange={(e) => setNewVersion({ description: e.target.value })}
            />
            <button
              className="btn-primary w-full"
              onClick={handleCreateVersion}
              disabled={creating || !newVersion.description.trim()}
            >
              {creating ? 'Creating...' : 'Create Version'}
            </button>
          </div>
        </div>

        {/* Version List */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Version History
            </h3>
          </div>
          <div className="border-t border-gray-200">
            <ul className="divide-y divide-gray-200">
              {versions.map((version) => (
                <li key={version.id} className="px-4 py-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-lg font-medium text-gray-900">
                        v{version.version_number}
                      </h4>
                      <p className="mt-1 text-sm text-gray-500">
                        {version.description}
                      </p>
                      <div className="mt-2 text-sm text-gray-500">
                        Created by {version.created_by.username} at{' '}
                        {new Date(version.created_at).toLocaleString()}
                      </div>
                    </div>
                    <button
                      className="btn-primary"
                      onClick={() => handleViewVersion(version.id)}
                    >
                      View Details
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <VersionDetailsDialog
        isOpen={dialogOpen}
        onClose={() => setDialogOpen(false)}
        version={selectedVersion}
      />
    </>
  )
} 