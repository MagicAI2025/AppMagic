import { useState } from 'react'
import { CodeEditor } from './CodeEditor'

interface ProjectGeneratorProps {
  onGenerate: (requirements: string) => void
  isGenerating: boolean
}

export function ProjectGenerator({ onGenerate, isGenerating }: ProjectGeneratorProps) {
  const [requirements, setRequirements] = useState('')
  
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="space-y-4">
        <div>
          <label 
            htmlFor="requirements" 
            className="block text-sm font-medium text-gray-700"
          >
            Project Requirements
          </label>
          <div className="mt-1">
            <textarea
              id="requirements"
              rows={4}
              className="input-primary"
              placeholder="Describe your project requirements..."
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
            />
          </div>
        </div>
        
        <button
          className="btn-primary w-full"
          onClick={() => onGenerate(requirements)}
          disabled={isGenerating || !requirements.trim()}
        >
          {isGenerating ? 'Generating...' : 'Generate Project'}
        </button>
      </div>
    </div>
  )
} 