import { SearchBar } from '@/components/search-bar'
import { Hero } from '@/components/hero'

export default function Home() {
  return (
    <main className="min-h-screen bg-pink-100">
      <div className="absolute inset-0 bg-grid-black/[0.02] -z-10" />
      <Hero />
      <div className="container mx-auto px-4 py-8">
        <SearchBar />
      </div>
    </main>
  )
}

