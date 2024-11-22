import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import ReactMarkdown from 'react-markdown'

interface ResultsCardProps {
  content: string
}

export function ResultsCard({ content }: ResultsCardProps) {
  // Check if the content is HTML
  const isHtml = content.trim().startsWith('<')

  return (
    <Card className="w-full mt-8">
      <CardHeader>
        <CardTitle>Search Results</CardTitle>
      </CardHeader>
      <CardContent>
        {isHtml ? (
          <div dangerouslySetInnerHTML={{ __html: content }} />
        ) : (
          <div className="prose dark:prose-invert max-w-none">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

