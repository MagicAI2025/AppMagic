import React, { useRef } from 'react'
import Editor from '@monaco-editor/react'
import { PencilIcon, ArrowUturnLeftIcon, ArrowUturnRightIcon } from '@heroicons/react/24/outline'

interface CodeEditorProps {
  value: string
  language: string
  onChange: (value: string) => void
  readOnly?: boolean
}

export function CodeEditor({ value, language, onChange, readOnly = false }: CodeEditorProps) {
  const editorRef = useRef(null)
  
  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor
  }
  
  const handleFormat = () => {
    if (editorRef.current) {
      editorRef.current.trigger('', 'editor.action.formatDocument')
    }
  }

  const handleUndo = () => {
    editorRef.current?.trigger('', 'undo')
  }

  const handleRedo = () => {
    editorRef.current?.trigger('', 'redo')
  }
  
  return (
    <div className="border border-gray-200 rounded-lg">
      <div className="px-4 py-2 bg-gray-50 flex justify-between items-center border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <button 
            className="inline-flex items-center p-1 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            title="Format Document"
          >
            <PencilIcon className="h-5 w-5" />
          </button>
          <button
            className="inline-flex items-center p-1 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            title="Undo"
          >
            <ArrowUturnLeftIcon className="h-5 w-5" />  
          </button>
          <button
            className="inline-flex items-center p-1 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            title="Redo"  
          >
            <ArrowUturnRightIcon className="h-5 w-5" />
          </button>
        </div>
        <div className="flex items-center space-x-2">
          <button
            className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Save
          </button>
        </div>
      </div>
      <Editor
        height="600px"
        defaultLanguage={language.toLowerCase()}
        value={value}
        theme="vs"
        onChange={(value) => onChange(value || '')}
        onMount={handleEditorDidMount}
        options={{
          readOnly,
          minimap: { enabled: true },
          scrollBeyondLastLine: false,
          fontSize: 14,
          tabSize: 2,
          automaticLayout: true
        }}
      />
    </div>
  )
} 