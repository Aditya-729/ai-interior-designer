'use client'

import { motion, HTMLMotionProps } from 'framer-motion'
import { ReactNode } from 'react'
import { fadeUp, getVariants } from '@/lib/motion'

interface AnimatedTextProps extends HTMLMotionProps<'div'> {
  children: ReactNode
  delay?: number
}

export default function AnimatedText({
  children,
  delay = 0,
  ...props
}: AnimatedTextProps) {
  const variants = getVariants(fadeUp)

  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate="visible"
      transition={{ delay }}
      {...props}
    >
      {children}
    </motion.div>
  )
}
