'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useEffect, useState } from 'react'
import { Loader2, Sparkles, Wand2, Image as ImageIcon, Zap } from 'lucide-react'
import { fadeIn, crossFade, getVariants } from '@/lib/motion'

interface StageOverlayProps {
  isVisible: boolean
  stage: 'uploading' | 'analyzing' | 'planning' | 'fetching' | 'editing' | null
  progress?: number
}

const stageConfig = {
  uploading: {
    label: 'Uploading your image...',
    icon: ImageIcon,
    color: 'text-blue-500',
  },
  analyzing: {
    label: 'Understanding your room...',
    icon: Sparkles,
    color: 'text-purple-500',
  },
  planning: {
    label: 'Planning your edits...',
    icon: Wand2,
    color: 'text-pink-500',
  },
  fetching: {
    label: 'Fetching design ideas...',
    icon: Sparkles,
    color: 'text-indigo-500',
  },
  editing: {
    label: 'Editing image on GPU...',
    icon: Zap,
    color: 'text-orange-500',
  },
}

export default function StageOverlay({ isVisible, stage, progress }: StageOverlayProps) {
  const [mounted, setMounted] = useState(false)
  const config = stage ? stageConfig[stage] : null

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <AnimatePresence>
      {isVisible && config && (
        <motion.div
          variants={getVariants(fadeIn)}
          initial="hidden"
          animate="visible"
          exit="hidden"
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          style={{ willChange: 'opacity' }}
        >
          <motion.div
            variants={getVariants({
              hidden: { opacity: 0, scale: 0.9, y: 20 },
              visible: {
                opacity: 1,
                scale: 1,
                y: 0,
                transition: { duration: 0.4, ease: [0.4, 0, 0.2, 1] },
              },
            })}
            initial="hidden"
            animate="visible"
            className="bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4"
            style={{
              background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%)',
            }}
          >
            <div className="flex flex-col items-center space-y-6">
              {/* Animated Icon */}
              <motion.div
                animate={{
                  rotate: [0, 360],
                  scale: [1, 1.1, 1],
                }}
                transition={{
                  rotate: { duration: 2, repeat: Infinity, ease: 'linear' },
                  scale: { duration: 1.5, repeat: Infinity, ease: 'easeInOut' },
                }}
                className={`${config.color} relative`}
              >
                <config.icon className="w-12 h-12" />
                <motion.div
                  className={`absolute inset-0 ${config.color.replace('text-', 'bg-')} rounded-full opacity-20 blur-xl`}
                  animate={{
                    scale: [1, 1.5, 1],
                    opacity: [0.2, 0.4, 0.2],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: 'easeInOut',
                  }}
                />
              </motion.div>

              {/* Animated Text */}
              <AnimatePresence mode="wait">
                <motion.div
                  key={stage}
                  variants={getVariants(crossFade)}
                  initial="hidden"
                  animate="visible"
                  exit="hidden"
                  className="text-center"
                >
                  <p className="text-lg font-semibold text-gray-900">{config.label}</p>
                </motion.div>
              </AnimatePresence>

              {/* Progress Bar */}
              {progress !== undefined && (
                <motion.div
                  className="w-full h-2 bg-gray-200 rounded-full overflow-hidden"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <motion.div
                    className={`h-full ${config.color.replace('text-', 'bg-')} rounded-full`}
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{
                      duration: 0.3,
                      ease: [0.4, 0, 0.2, 1],
                    }}
                    style={{
                      background: `linear-gradient(90deg, ${config.color.replace('text-', '')} 0%, ${config.color.replace('text-', '')} 100%)`,
                    }}
                  />
                </motion.div>
              )}

              {/* Loading Dots */}
              <div className="flex space-x-2">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className={`w-2 h-2 ${config.color.replace('text-', 'bg-')} rounded-full`}
                    animate={{
                      y: [0, -8, 0],
                      opacity: [0.5, 1, 0.5],
                    }}
                    transition={{
                      duration: 0.6,
                      repeat: Infinity,
                      delay: i * 0.2,
                      ease: 'easeInOut',
                    }}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
