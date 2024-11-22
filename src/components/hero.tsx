import Image from 'next/image'

export function Hero() {
  return (
    <div className="bg-gradient-to-r from-purple-700 to-indigo-700 text-white py-12 md:py-20">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center space-y-6">
          <Image
            src="/logo.png"
            alt="Compliance Officer Logo"
            width={100}
            height={100}
            className="rounded-full bg-white p-2"
          />
          <h1 className="text-4xl md:text-6xl font-bold text-center">Sei AI-powered Regulatory Compliance Platform </h1>
          <p className="mt-4 text-xl text-center max-w-2xl mx-auto">
            Compliance Officer at your service
          </p>
        </div>
      </div>
    </div>
  )
}

