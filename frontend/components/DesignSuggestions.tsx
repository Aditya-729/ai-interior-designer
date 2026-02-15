'use client'

import { useState, useEffect } from 'react'
import { Lightbulb, Sparkles } from 'lucide-react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { staggerContainer, staggerItem, getVariants } from '@/lib/motion'

interface DesignSuggestionsProps {
  imageId: string | null
  projectId: string | null
}

export default function DesignSuggestions({
  imageId,
  projectId,
}: DesignSuggestionsProps) {
  const [suggestions, setSuggestions] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [cards, setCards] = useState<any[]>([])

  useEffect(() => {
    if (imageId) {
      loadSuggestions()
    }
  }, [imageId])

  const loadSuggestions = async () => {
    setLoading(true)
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
      const response = await axios.post(
        `${apiBase}/api/v1/fetch-design-knowledge`,
        {
          user_request: 'Get design suggestions',
          image_id: imageId,
          project_id: projectId,
        }
      )
      setSuggestions(response.data.recommendations || response.data.raw_response)
      
      // Parse into cards (simple implementation)
      const lines = (response.data.recommendations || '').split('\n').filter(l => l.trim())
      setCards(lines.slice(0, 5).map((line, i) => ({ id: i, text: line })))
    } catch (error) {
      console.error('Failed to load suggestions:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      variants={getVariants({
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
      })}
      initial="hidden"
      animate="visible"
      className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/20"
      style={{
        background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
      }}
    >
      <div className="flex items-center gap-2 mb-4">
        <motion.div
          animate={{
            rotate: [0, 10, -10, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            repeatDelay: 3,
            ease: 'easeInOut',
          }}
        >
          <Lightbulb className="w-5 h-5 text-yellow-500" />
        </motion.div>
        <h2 className="text-xl font-semibold">Design Suggestions</h2>
      </div>
      
      {loading ? (
        <div className="flex items-center justify-center py-8">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          >
            <Sparkles className="w-6 h-6 text-primary-500" />
          </motion.div>
        </div>
      ) : cards.length > 0 ? (
        <motion.div
          variants={getVariants(staggerContainer)}
          initial="hidden"
          animate="visible"
          className="space-y-3"
        >
          {cards.map((card, index) => (
            <motion.div
              key={card.id}
              variants={getVariants(staggerItem)}
              whileHover={{ scale: 1.02, y: -2 }}
              className="p-4 bg-gradient-to-r from-primary-50 to-purple-50 rounded-lg border border-primary-100"
              style={{
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
              }}
            >
              <div className="flex items-start gap-3">
                <motion.div
                  animate={{
                    scale: [1, 1.2, 1],
                  }}
                  transition={{
                    duration: 0.5,
                    delay: index * 0.1,
                  }}
                  className="mt-1"
                >
                  <Sparkles className="w-4 h-4 text-primary-500" />
                </motion.div>
                <p className="text-sm text-gray-700 flex-1">{card.text}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      ) : suggestions ? (
        <div className="text-sm text-gray-600 whitespace-pre-wrap">
          {suggestions}
        </div>
      ) : (
        <p className="text-gray-500 text-sm">
          Upload an image to get design suggestions
        </p>
      )}
    </motion.div>
  )
}
