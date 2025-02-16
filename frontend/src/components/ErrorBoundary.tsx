import React from 'react'
import { toast } from 'react-hot-toast'

interface Props {
  children: React.ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(_: Error): State {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error:', error, errorInfo)
    toast.error('Something went wrong')
    this.setState({ 
      hasError: true,
      error: new Error(`${error.toString()} \n ${errorInfo.componentStack}`) 
    })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Something went wrong
            </h1>
            <button
              className="btn-primary"
              onClick={() => this.setState({ hasError: false })}
            >
              Try again
            </button>
            {this.state.error && (
              <details className="mt-4 text-sm text-red-600">
                <summary>Error Details</summary>
                <pre className="whitespace-pre-wrap mt-2">
                  {this.state.error.toString()}
                </pre>
              </details>
            )}
          </div>
        </div>
      )
    }

    return this.props.children
  }
} 