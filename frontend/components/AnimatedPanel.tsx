'use client'

import { motion, HTMLMotionProps } from 'framer-motion'
import { ReactNode } from 'react'
import { panelSlide, getVariants } from '@/lib/motion'

interface AnimatedPanelProps extends HTMLMotionProps<'div'> {
  children: ReactNode
  isOpen: boolean
}

export default function AnimatedPanel({
  children,
  isOpen,
  ...props
}: AnimatedPanelProps) {
  const variants = getVariants(panelSlide)

  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate={isOpen ? 'visible' : 'hidden'}
      style={{ overflow: 'hidden' }}
      {...props}
    >
      {children}
    </motion.div>
  )
}
