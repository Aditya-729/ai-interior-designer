'use client'

import { useState } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'
import { fadeUp, getVariants } from '@/lib/motion'

interface TextInputProps {
  onSubmit: (text: string) => Promise<void>
  disabled?: boolean
}

export default function TextInput({ onSubmit, disabled }: TextInputProps) {
  const [input, setInput] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || disabled || isSubmitting) return

    setIsSubmitting(true)
    try {
      await onSubmit(input)
      setInput('')
    } catch (error) {
      console.error('Submit failed:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <motion.form
      variants={getVariants(fadeUp)}
      initial="hidden"
      animate="visible"
      onSubmit={handleSubmit}
      className="space-y-2"
    >
      <motion.textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your design changes... (e.g., 'Make the wall warm beige, change the floor tiles to marble')"
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none transition-all"
        style={{
          backdropFilter: 'blur(10px)',
        }}
        rows={4}
        disabled={disabled || isSubmitting}
        whileFocus={{ scale: 1.01 }}
      />
      <div className="flex justify-end">
        <motion.button
          type="submit"
          disabled={!input.trim() || disabled || isSubmitting}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 px-6 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Apply Changes
            </>
          )}
        </motion.button>
      </div>
    </motion.form>
  )
}
