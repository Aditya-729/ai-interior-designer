'use client'

import { useState, useRef, useEffect } from 'react'
import { Mic, MicOff, Loader2 } from 'lucide-react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'

interface VoiceInputProps {
  onTranscriptionComplete: (text: string) => void
}

export default function VoiceInput({ onTranscriptionComplete }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isTranscribing, setIsTranscribing] = useState(false)
  const [waveform, setWaveform] = useState<number[]>([])
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const animationFrameRef = useRef<number>()

  // Generate waveform data
  useEffect(() => {
    if (isRecording) {
      const generateWaveform = () => {
        const bars = Array.from({ length: 20 }, () => Math.random() * 100)
        setWaveform(bars)
        animationFrameRef.current = requestAnimationFrame(generateWaveform)
      }
      generateWaveform()
    } else {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
      setWaveform([])
    }
  }, [isRecording])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        await transcribeAudio(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error starting recording:', error)
      alert('Failed to access microphone')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const transcribeAudio = async (audioBlob: Blob) => {
    setIsTranscribing(true)
    try {
      const formData = new FormData()
      formData.append('file', audioBlob, 'recording.webm')

      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
      const response = await axios.post(
        `${apiBase}/api/v1/transcribe`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )

      onTranscriptionComplete(response.data.text)
    } catch (error) {
      console.error('Transcription failed:', error)
      alert('Failed to transcribe audio')
    } finally {
      setIsTranscribing(false)
    }
  }

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Voice Button */}
      <motion.button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={isTranscribing}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`
          relative flex items-center gap-2 px-6 py-3 rounded-lg font-medium
          transition-colors overflow-hidden
          ${isRecording
            ? 'bg-red-500 hover:bg-red-600 text-white'
            : 'bg-primary-500 hover:bg-primary-600 text-white'
          }
          disabled:opacity-50 disabled:cursor-not-allowed
        `}
      >
        {/* Animated glow ring when recording */}
        {isRecording && (
          <motion.div
            className="absolute inset-0 rounded-lg bg-red-400"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.5, 0.8, 0.5],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
            style={{ filter: 'blur(10px)' }}
          />
        )}

        {isTranscribing ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin relative z-10" />
            <span className="relative z-10">Transcribing...</span>
          </>
        ) : isRecording ? (
          <>
            <MicOff className="w-5 h-5 relative z-10" />
            <span className="relative z-10">Stop Recording</span>
          </>
        ) : (
          <>
            <Mic className="w-5 h-5 relative z-10" />
            <span className="relative z-10">Start Voice Input</span>
          </>
        )}
      </motion.button>

      {/* Waveform Animation */}
      <AnimatePresence>
        {isRecording && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="flex items-center justify-center gap-1 h-12 w-full"
          >
            {waveform.map((height, i) => (
              <motion.div
                key={i}
                className="bg-primary-500 rounded-full"
                style={{ width: '4px' }}
                animate={{
                  height: `${height}%`,
                }}
                transition={{
                  duration: 0.3,
                  ease: 'easeOut',
                }}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Status Text */}
      <AnimatePresence mode="wait">
        {isRecording && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="flex items-center gap-2 text-red-500"
          >
            <motion.div
              className="w-3 h-3 bg-red-500 rounded-full"
              animate={{
                scale: [1, 1.2, 1],
                opacity: [1, 0.7, 1],
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
            <span className="text-sm">Recording...</span>
          </motion.div>
        )}
        {isTranscribing && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="flex items-center gap-2 text-primary-600"
          >
            <div className="flex space-x-1">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-2 h-2 bg-primary-500 rounded-full"
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
            <span className="text-sm">Transcribing your request…</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
