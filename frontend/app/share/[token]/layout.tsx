import { Metadata } from 'next'

export async function generateMetadata({ params }: { params: { token: string } }): Promise<Metadata> {
  // Fetch share data for metadata
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
  
  try {
    const response = await fetch(`${apiBase}/api/v1/share/${params.token}`, {
      next: { revalidate: 3600 } // Cache for 1 hour
    })
    
    if (response.ok) {
      const data = await response.json()
      const title = `${data.project.name} - AI Interior Design Preview`
      const description = data.version.user_prompt || 'AI-powered interior design transformation'
      const image = data.edited_image || data.original_image
      
      return {
        title,
        description,
        openGraph: {
          title,
          description,
          images: image ? [image] : [],
          type: 'website',
        },
        twitter: {
          card: 'summary_large_image',
          title,
          description,
          images: image ? [image] : [],
        },
      }
    }
  } catch (error) {
    // Fallback metadata
  }
  
  return {
    title: 'AI Interior Design Preview',
    description: 'AI-powered interior design transformation',
  }
}

export default function ShareLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
