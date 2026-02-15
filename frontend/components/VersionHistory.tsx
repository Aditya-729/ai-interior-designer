'use client'

import { Clock, Share2, Download } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { staggerContainer, staggerItem, glow, getVariants } from '@/lib/motion'
import { useState } from 'react'
import axios from 'axios'
import ExportButton from './ExportButton'

interface VersionHistoryProps {
  versions: any[]
  projectId: string | null
  onVersionSelect: (version: any) => void
}

export default function VersionHistory({
  versions,
  projectId,
  onVersionSelect,
}: VersionHistoryProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [sharing, setSharing] = useState<string | null>(null)

  const handleShare = async (versionId: string) => {
    if (!projectId) return
    
    setSharing(versionId)
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
      const response = await axios.post(
        `${apiBase}/api/v1/projects/${projectId}/share`,
        { version_id: versionId },
        { withCredentials: true }
      )
      
      // Copy to clipboard
      await navigator.clipboard.writeText(response.data.share_url)
      alert('Share link copied to clipboard!')
    } catch (error) {
      console.error('Share failed:', error)
      alert('Failed to create share link')
    } finally {
      setSharing(null)
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
      <h2 className="text-xl font-semibold mb-4">Version History</h2>
      {versions.length === 0 ? (
        <p className="text-gray-500 text-sm">No versions yet</p>
      ) : (
        <motion.div
          variants={getVariants(staggerContainer)}
          initial="hidden"
          animate="visible"
          className="space-y-2"
        >
          <AnimatePresence>
            {versions.map((version, index) => (
              <motion.button
                key={version.id}
                variants={getVariants(staggerItem)}
                initial="hidden"
                animate="visible"
                exit={{ opacity: 0, scale: 0.9 }}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  setSelectedId(version.id)
                  onVersionSelect(version)
                }}
                className={`
                  w-full text-left p-3 rounded-lg transition-all
                  border-2
                  ${selectedId === version.id
                    ? 'bg-primary-50 border-primary-500 shadow-lg'
                    : 'hover:bg-gray-50 border-transparent hover:border-gray-200'
                  }
                `}
                style={{
                  willChange: 'transform',
                }}
              >
                <motion.div
                  animate={selectedId === version.id ? {
                    boxShadow: '0 0 20px rgba(59, 130, 246, 0.3)',
                  } : {}}
                  className="flex items-center gap-2 mb-1"
                >
                  <Clock className="w-4 h-4 text-gray-400" />
                  <span className="font-medium">
                    Version {versions.length - index}
                  </span>
                </motion.div>
                {version.user_prompt && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="text-sm text-gray-600 truncate"
                  >
                    {version.user_prompt}
                  </motion.p>
                )}
                {version.created_at && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-xs text-gray-400 mt-1"
                  >
                    {new Date(version.created_at).toLocaleString()}
                  </motion.p>
                )}
                
                {/* Actions */}
                <div className="flex items-center gap-2 mt-2">
                  {projectId && (
                    <>
                      <motion.button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleShare(version.id)
                        }}
                        disabled={sharing === version.id}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="p-1.5 text-primary-500 hover:bg-primary-50 rounded transition-colors"
                        title="Share"
                      >
                        <Share2 className="w-4 h-4" />
                      </motion.button>
                      <ExportButton projectId={projectId} versionId={version.id} />
                    </>
                  )}
                </div>
              </motion.button>
            ))}
          </AnimatePresence>
        </motion.div>
      )}
    </motion.div>
  )
}
