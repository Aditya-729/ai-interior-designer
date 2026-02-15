'use client'

import { useState, useEffect } from 'react'
import ImageUpload from '@/components/ImageUpload'
import VoiceInput from '@/components/VoiceInput'
import TextInput from '@/components/TextInput'
import EditPreview from '@/components/EditPreview'
import ProjectDashboard from '@/components/ProjectDashboard'
import VersionHistory from '@/components/VersionHistory'
import DesignSuggestions from '@/components/DesignSuggestions'
import StageOverlay from '@/components/StageOverlay'
import AnimatedContainer from '@/components/AnimatedContainer'
import AnimatedText from '@/components/AnimatedText'
import { motion } from 'framer-motion'
import { fadeUp, slideLeft, slideRight, scaleIn, staggerContainer, staggerItem, getVariants } from '@/lib/motion'

export default function Home() {
  const [currentImage, setCurrentImage] = useState<string | null>(null)
  const [imageId, setImageId] = useState<string | null>(null)
  const [projectId, setProjectId] = useState<string | null>(null)
  const [versions, setVersions] = useState<any[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [stage, setStage] = useState<'uploading' | 'analyzing' | 'planning' | 'fetching' | 'editing' | null>(null)
  const [progress, setProgress] = useState(0)
  const [clientId] = useState(() => `client-${Date.now()}`)

  // WebSocket connection for real-time updates
  useEffect(() => {
    let ws: WebSocket | null = null
    
    const connectWebSocket = async () => {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
      
      // Get WebSocket URL
      let wsUrl = process.env.NEXT_PUBLIC_WS_URL
      if (!wsUrl) {
        try {
          const response = await fetch(`${apiBase}/api/v1/system/ws-url`)
          const data = await response.json()
          wsUrl = data.ws_url
        } catch {
          // Fallback to default
          wsUrl = apiBase.replace('http://', 'ws://').replace('https://', 'wss://')
        }
      }
      
      ws = new WebSocket(`${wsUrl}/${clientId}`)
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        // Update stage based on WebSocket events
        if (data.status === 'transcribing') {
          setStage('analyzing')
          setProgress(data.progress || 0)
        } else if (data.status === 'processing') {
          if (data.message?.includes('Planning')) {
            setStage('planning')
          } else if (data.message?.includes('design')) {
            setStage('fetching')
          } else if (data.message?.includes('AI model')) {
            setStage('editing')
          }
          setProgress(data.progress || 0)
        } else if (data.status === 'completed') {
          setStage(null)
          setProgress(100)
          setTimeout(() => {
            setProgress(0)
            setIsProcessing(false)
          }, 1000)
        } else if (data.status === 'error') {
          setStage(null)
          setIsProcessing(false)
        }
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      ws.onclose = () => {
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000)
      }
    }
    
    connectWebSocket()
    
    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [clientId])

  const handleImageUploaded = (imageUrl: string, id: string) => {
    setCurrentImage(imageUrl)
    setImageId(id)
    setStage('analyzing')
  }

  const handleEditSubmit = async (prompt: string) => {
    if (!imageId) return
    
    setIsProcessing(true)
    setStage('planning')
    setProgress(10)

    try {
      // 1. Analyze scene
      setStage('analyzing')
      setProgress(20)
      const analysisResponse = await fetch(`http://localhost:8000/api/v1/analyze-scene`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_id: imageId }),
      })
      const analysis = await analysisResponse.json()

      // 2. Plan edits
      setStage('planning')
      setProgress(40)
      const planResponse = await fetch(`${apiBase}/api/v1/plan-edits`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_prompt: prompt,
          image_id: imageId,
          project_id: projectId,
        }),
      })
      const editPlan = await planResponse.json()

      // 3. Fetch design knowledge
      setStage('fetching')
      setProgress(60)
      await fetch(`${apiBase}/api/v1/fetch-design-knowledge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_request: prompt,
          image_id: imageId,
          project_id: projectId,
        }),
      })

      // 4. Run inference
      setStage('editing')
      setProgress(80)
      const inferenceResponse = await fetch(`${apiBase}/api/v1/run-inpainting`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_id: imageId,
          edit_plan: editPlan,
          project_id: projectId,
          client_id: clientId,
        }),
      })
      const result = await inferenceResponse.json()

      // 5. Update versions
      setVersions([{ ...result, user_prompt: prompt }, ...versions])
      setProgress(100)
      setStage(null)
      
      setTimeout(() => {
        setIsProcessing(false)
        setProgress(0)
      }, 1000)
    } catch (error) {
      console.error('Edit failed:', error)
      setStage(null)
      setIsProcessing(false)
      setProgress(0)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 relative overflow-hidden">
      {/* Subtle noise overlay for premium feel */}
      <div 
        className="fixed inset-0 opacity-[0.015] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />

      {/* Stage Overlay */}
      <StageOverlay isVisible={isProcessing && stage !== null} stage={stage} progress={progress} />

      <div className="container mx-auto px-4 py-8 relative z-10">
        {/* Animated Header */}
        <AnimatedContainer>
          <motion.header
            variants={getVariants(staggerContainer)}
            initial="hidden"
            animate="visible"
            className="mb-12"
          >
            <motion.h1
              variants={getVariants(fadeUp)}
              className="text-5xl font-bold text-gray-900 mb-4 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent"
            >
              AI Interior Designer
            </motion.h1>
            <motion.p
              variants={getVariants(fadeUp)}
              transition={{ delay: 0.1 }}
              className="text-xl text-gray-600"
            >
              Transform your rooms with AI-powered design modifications
            </motion.p>
          </motion.header>
        </AnimatedContainer>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input */}
          <motion.div
            variants={getVariants(slideLeft)}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
            className="lg:col-span-2 space-y-6"
          >
            {/* Upload Card */}
            <motion.div
              variants={getVariants(scaleIn)}
              initial="hidden"
              animate="visible"
              transition={{ delay: 0.3 }}
              className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/20"
              style={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
                boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
              }}
            >
              <h2 className="text-2xl font-semibold mb-4">Upload Room Image</h2>
              <ImageUpload onImageUploaded={handleImageUploaded} />
            </motion.div>

            {currentImage && (
              <>
                {/* Edit Instructions Card */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/20"
                  style={{
                    background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
                    boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
                  }}
                >
                  <h2 className="text-2xl font-semibold mb-4">Edit Instructions</h2>
                  <div className="space-y-4">
                    <VoiceInput
                      onTranscriptionComplete={(text) => {
                        handleEditSubmit(text)
                      }}
                    />
                    <TextInput
                      onSubmit={handleEditSubmit}
                      disabled={isProcessing}
                    />
                  </div>
                </motion.div>

                {/* Preview Card */}
                <motion.div
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                >
                  <EditPreview
                    originalImage={currentImage}
                    editedImage={versions[0]?.image_url}
                    isProcessing={isProcessing}
                  />
                </motion.div>
              </>
            )}
          </motion.div>

          {/* Right Column - Sidebar */}
          <motion.div
            variants={getVariants(slideRight)}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            <ProjectDashboard
              projectId={projectId}
              onProjectSelect={(id) => setProjectId(id)}
            />

            <VersionHistory
              versions={versions}
              projectId={projectId}
              onVersionSelect={(version) => {
                // Load version
              }}
            />

            <DesignSuggestions
              imageId={imageId}
              projectId={projectId}
            />
          </motion.div>
        </div>
      </div>
    </main>
  )
}
