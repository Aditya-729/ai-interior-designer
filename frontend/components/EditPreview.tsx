'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { Loader2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { zoomReveal, crossFade, getVariants } from '@/lib/motion'

interface EditPreviewProps {
  originalImage: string
  editedImage?: string | null
  isProcessing?: boolean
}

export default function EditPreview({
  originalImage,
  editedImage,
  isProcessing,
}: EditPreviewProps) {
  const [sliderPosition, setSliderPosition] = useState(50)
  const [showResult, setShowResult] = useState(false)

  useEffect(() => {
    if (editedImage && !isProcessing) {
      setShowResult(true)
      // Subtle brightness flash on reveal
      setTimeout(() => setShowResult(false), 500)
    }
  }, [editedImage, isProcessing])

  if (isProcessing) {
    return (
      <motion.div
        variants={getVariants(zoomReveal)}
        initial="hidden"
        animate="visible"
        className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/20"
        style={{
          background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        }}
      >
        <h2 className="text-2xl font-semibold mb-4">Processing Edit...</h2>
        
        {/* Shimmer skeleton animation */}
        <div className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden">
          {/* Shimmer effect */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
            animate={{
              x: ['-100%', '100%'],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: 'linear',
            }}
            style={{ width: '50%' }}
          />
          
          {/* Blurred preview */}
          <div className="absolute inset-0">
            <Image
              src={originalImage}
              alt="Original"
              fill
              className="object-contain blur-sm opacity-50"
            />
          </div>
          
          {/* Noise overlay */}
          <motion.div
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
            }}
            animate={{
              opacity: [0.05, 0.15, 0.05],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
          
          <div className="absolute inset-0 flex items-center justify-center">
            <Loader2 className="w-12 h-12 text-primary-500 animate-spin" />
          </div>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      variants={getVariants(zoomReveal)}
      initial="hidden"
      animate="visible"
      className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/20"
      style={{
        background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
      }}
    >
      <h2 className="text-2xl font-semibold mb-4">Preview</h2>
      {editedImage ? (
        <motion.div
          initial={{ opacity: 0, scale: 1.02 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden group"
        >
          {/* Brightness flash overlay */}
          <AnimatePresence>
            {showResult && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.3 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="absolute inset-0 bg-white z-20 pointer-events-none"
              />
            )}
          </AnimatePresence>

          {/* Original image */}
          <div className="absolute inset-0">
            <Image
              src={originalImage}
              alt="Original"
              fill
              className="object-contain"
            />
          </div>
          
          {/* Edited image with slider */}
          <motion.div
            className="absolute inset-0 overflow-hidden"
            style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
            initial={{ clipPath: 'inset(0 100% 0 0)' }}
            animate={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
            transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
          >
            <Image
              src={editedImage}
              alt="Edited"
              fill
              className="object-contain"
            />
          </motion.div>
          
          {/* Slider handle */}
          <motion.input
            type="range"
            min="0"
            max="100"
            value={sliderPosition}
            onChange={(e) => setSliderPosition(Number(e.target.value))}
            className="absolute bottom-4 left-4 right-4 w-auto z-10 accent-primary-500"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          />
          
          {/* Labels */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm text-white px-3 py-1 rounded text-sm"
          >
            Original
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            className="absolute top-4 right-4 bg-black/50 backdrop-blur-sm text-white px-3 py-1 rounded text-sm"
          >
            Edited
          </motion.div>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative aspect-video bg-gray-100 rounded-lg overflow-hidden"
        >
          <Image
            src={originalImage}
            alt="Original"
            fill
            className="object-contain"
          />
        </motion.div>
      )}
    </motion.div>
  )
}
