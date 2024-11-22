'use client'

import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Loader2 } from 'lucide-react'
import { ResultsCard } from '@/components/result-card'

export function SearchBar() {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setResults(null)
    setError(null)
    
    const apiUrl = 'https://brrxlylpkap4roolnvdvfkjcyu0izgtq.lambda-url.us-east-1.on.aws/'
    
    try {
      const response = await fetch(`${apiUrl}?url=${encodeURIComponent(query)}`)

      console.log(response)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.text()
      setResults(data)
    } catch (error) {
      console.error('Search error:', error)
      setError('An error occurred while fetching results. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="w-full max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-lg mx-auto">
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <div className="relative flex-grow">
          <Search className="absolute left-2 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Enter a URL to generate compliance report ( Example: https://www.mercury.com/"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-8"
            disabled={isLoading}
          />
        </div>
        <Button type="submit" disabled={isLoading}>
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Searching...
            </>
          ) : (
            'Search'
          )}
        </Button>
      </form>
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      {results && <ResultsCard content={results} />}
    </div>
  )
}

