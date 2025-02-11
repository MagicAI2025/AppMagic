import React, { useState, useEffect } from 'react'
import { useAuthStore } from '@/store/useAuthStore'
import api from '@/utils/api'
import { toast } from 'react-hot-toast'
import { Comment } from '../types'

interface Comment {
  id: number
  content: string
  user: {
    id: number
    username: string
  }
  created_at: string
  replies: Array<{
    id: number
    content: string
    user: {
      id: number
      username: string
    }
    created_at: string
  }>
}

interface ProjectCommentsProps {
  projectId: number
}

export function ProjectComments({ projectId }: ProjectCommentsProps) {
  const [comments, setComments] = useState<Comment[]>([])
  const [newComment, setNewComment] = useState('')
  const [loading, setLoading] = useState(false)
  const { user } = useAuthStore()
  
  useEffect(() => {
    fetchComments()
  }, [projectId])
  
  const fetchComments = async () => {
    try {
      const response = await api.get(`/api/projects/${projectId}/comments`)
      setComments(response.data.comments)
    } catch (error) {
      toast.error('Failed to load comments')
    }
  }
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newComment.trim()) return
    
    try {
      setLoading(true)
      await api.post(`/api/projects/${projectId}/comments`, {
        content: newComment
      })
      setNewComment('')
      await fetchComments()
      toast.success('Comment posted successfully')
    } catch (error) {
      toast.error('Failed to post comment')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="space-y-6">
      {/* Comment Input */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="input-primary"
          rows={3}
          placeholder="Write your comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
        />
        <button
          type="submit"
          className="btn-primary"
          disabled={loading || !newComment.trim()}
        >
          {loading ? 'Posting...' : 'Post Comment'}
        </button>
      </form>
      
      {/* Comments List */}
      <div className="space-y-4">
        {comments.map((comment) => (
          <div key={comment.id} className="bg-white shadow rounded-lg p-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="font-medium">{comment.user.username}</span>
                <span className="text-gray-500 text-sm ml-2">
                  {new Date(comment.created_at).toLocaleString()}
                </span>
              </div>
            </div>
            <p className="mt-2 text-gray-700">{comment.content}</p>
            
            {/* Replies List */}
            {comment.replies.length > 0 && (
              <div className="mt-4 pl-4 border-l-2 border-gray-200 space-y-4">
                {comment.replies.map((reply) => (
                  <div key={reply.id}>
                    <div className="flex justify-between items-start">
                      <div>
                        <span className="font-medium">{reply.user.username}</span>
                        <span className="text-gray-500 text-sm ml-2">
                          {new Date(reply.created_at).toLocaleString()}
                        </span>
                      </div>
                    </div>
                    <p className="mt-1 text-gray-700">{reply.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
} 