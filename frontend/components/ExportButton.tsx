'use client'

import { Download } from 'lucide-react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { useState } from 'react'

interface ExportButtonProps {
  projectId: string
  versionId: string
}

export default function ExportButton({ projectId, versionId }: ExportButtonProps) {
  const [exporting, setExporting] = useState(false)

  const handleExport = async () => {
    setExporting(true)
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
      const response = await axios.get(
        `${apiBase}/api/v1/projects/${projectId}/versions/${versionId}/export`,
        {
          responseType: 'blob',
          withCredentials: true,
        }
      )

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `interior-design-${versionId}.jpg`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Failed to export image')
    } finally {
      setExporting(false)
    }
  }

  return (
    <motion.button
      onClick={handleExport}
      disabled={exporting}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="flex items-center gap-2 px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
    >
      <Download className="w-4 h-4" />
      {exporting ? 'Exporting...' : 'Export Image'}
    </motion.button>
  )
}
