'use client'

import { useState, useEffect } from 'react'
import { Folder, Plus } from 'lucide-react'
import { motion } from 'framer-motion'
import { staggerContainer, staggerItem, getVariants } from '@/lib/motion'

interface ProjectDashboardProps {
  projectId: string | null
  onProjectSelect: (id: string) => void
}

export default function ProjectDashboard({
  projectId,
  onProjectSelect,
}: ProjectDashboardProps) {
  const [projects, setProjects] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load projects (would use actual user ID in production)
    const loadProjects = async () => {
      try {
        // This would fetch from API with actual user ID
        // const response = await axios.get('/api/v1/projects?user_id=...')
        // setProjects(response.data)
      } catch (error) {
        console.error('Failed to load projects:', error)
      } finally {
        setLoading(false)
      }
    }

    loadProjects()
  }, [])

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
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Projects</h2>
        <motion.button
          whileHover={{ scale: 1.1, rotate: 90 }}
          whileTap={{ scale: 0.9 }}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
        </motion.button>
      </div>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : projects.length === 0 ? (
        <p className="text-gray-500 text-sm">No projects yet</p>
      ) : (
        <motion.div
          variants={getVariants(staggerContainer)}
          initial="hidden"
          animate="visible"
          className="space-y-2"
        >
          {projects.map((project) => (
            <motion.button
              key={project.id}
              variants={getVariants(staggerItem)}
              whileHover={{ scale: 1.02, x: 4 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onProjectSelect(project.id)}
              className={`
                w-full text-left p-3 rounded-lg transition-all
                ${projectId === project.id
                  ? 'bg-primary-50 border-2 border-primary-500'
                  : 'hover:bg-gray-50 border-2 border-transparent'
                }
              `}
            >
              <div className="flex items-center gap-2">
                <Folder className="w-4 h-4 text-gray-400" />
                <span className="font-medium">{project.name}</span>
              </div>
            </motion.button>
          ))}
        </motion.div>
      )}
    </motion.div>
  )
}
