'use client'

import { motion, HTMLMotionProps } from 'framer-motion'
import { ReactNode } from 'react'
import { staggerContainer, getVariants } from '@/lib/motion'

interface AnimatedContainerProps extends HTMLMotionProps<'div'> {
  children: ReactNode
  stagger?: boolean
}

export default function AnimatedContainer({
  children,
  stagger = false,
  ...props
}: AnimatedContainerProps) {
  const variants = stagger ? getVariants(staggerContainer) : undefined

  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate="visible"
      {...props}
    >
      {children}
    </motion.div>
  )
}
