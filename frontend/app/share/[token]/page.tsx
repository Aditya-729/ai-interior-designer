'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { motion } from 'framer-motion'
import { fadeUp, getVariants } from '@/lib/motion'
import axios from 'axios'

export default function SharePage({ params }: { params: { token: string } }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [sliderPosition, setSliderPosition] = useState(50)

  useEffect(() => {
    const loadShareData = async () => {
      try {
        const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
        const response = await axios.get(
          `${apiBase}/api/v1/share/${params.token}`
        )
        setData(response.data)
      } catch (error) {
        console.error('Failed to load share data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadShareData()
  }, [params.token])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading shared design...</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Share link not found</h1>
          <p className="text-gray-600">This link may have expired or been removed.</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          variants={getVariants(fadeUp)}
          initial="hidden"
          animate="visible"
          className="max-w-4xl mx-auto"
        >
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              {data.project.name}
            </h1>
            {data.project.description && (
              <p className="text-gray-600">{data.project.description}</p>
            )}
            {data.version.user_prompt && (
              <p className="text-sm text-gray-500 mt-2">
                "{data.version.user_prompt}"
              </p>
            )}
          </div>

          {/* Before/After Slider */}
          <motion.div
            variants={getVariants(fadeUp)}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
            className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 mb-6 border border-white/20"
            style={{
              background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
              boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
            }}
          >
            <div className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden">
              {/* Original image */}
              {data.original_image && (
                <div className="absolute inset-0">
                  <Image
                    src={data.original_image}
                    alt="Original"
                    fill
                    className="object-contain"
                  />
                </div>
              )}
              
              {/* Edited image with slider */}
              {data.edited_image && (
                <motion.div
                  className="absolute inset-0 overflow-hidden"
                  style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
                  initial={{ clipPath: 'inset(0 100% 0 0)' }}
                  animate={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
                  transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
                >
                  <Image
                    src={data.edited_image}
                    alt="Edited"
                    fill
                    className="object-contain"
                  />
                </motion.div>
              )}
              
              {/* Slider */}
              <input
                type="range"
                min="0"
                max="100"
                value={sliderPosition}
                onChange={(e) => setSliderPosition(Number(e.target.value))}
                className="absolute bottom-4 left-4 right-4 w-auto z-10 accent-primary-500"
              />
              
              {/* Labels */}
              <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm text-white px-3 py-1 rounded text-sm">
                Before
              </div>
              <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm text-white px-3 py-1 rounded text-sm">
                After
              </div>
            </div>
          </motion.div>

          {/* Design Notes */}
          {data.edit_plan && (
            <motion.div
              variants={getVariants(fadeUp)}
              initial="hidden"
              animate="visible"
              transition={{ delay: 0.3 }}
              className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/20"
              style={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
                boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
              }}
            >
              <h2 className="text-2xl font-semibold mb-4">Design Changes</h2>
              <div className="space-y-2">
                {data.edit_plan.edits && data.edit_plan.edits.map((edit: any, index: number) => (
                  <div key={index} className="p-3 bg-primary-50 rounded-lg">
                    <p className="text-sm text-gray-700">
                      <span className="font-medium">{edit.object}</span>: {edit.operation}
                      {edit.color && ` - ${edit.color}`}
                      {edit.material && ` - ${edit.material}`}
                    </p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Footer */}
          <motion.div
            variants={getVariants(fadeUp)}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.4 }}
            className="text-center mt-8 text-sm text-gray-500"
          >
            <p>Created with AI Interior Designer</p>
            <p className="mt-1">
              {new Date(data.version.created_at).toLocaleDateString()}
            </p>
          </motion.div>
        </motion.div>
      </div>
    </main>
  )
}
