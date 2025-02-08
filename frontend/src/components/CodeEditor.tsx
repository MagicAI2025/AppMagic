import React, { useRef } from 'react'
import Editor from '@monaco-editor/react'

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
  
  return (
    <Editor
      height="600px"
      defaultLanguage={language.toLowerCase()}
      value={value}
      theme="vs-dark"
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
  )
} 