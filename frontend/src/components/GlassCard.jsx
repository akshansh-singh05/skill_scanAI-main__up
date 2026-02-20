import { motion } from 'framer-motion'

const GlassCard = ({ 
  children, 
  className = '',
  blur = 'xl',
  opacity = 10,
  border = true,
  hover = true,
  animate = true,
  delay = 0,
  ...props
}) => {
  const blurClasses = {
    sm: 'backdrop-blur-sm',
    md: 'backdrop-blur-md',
    lg: 'backdrop-blur-lg',
    xl: 'backdrop-blur-xl',
    '2xl': 'backdrop-blur-2xl',
    '3xl': 'backdrop-blur-3xl',
  }

  const opacityClasses = {
    5: 'bg-white/5',
    10: 'bg-white/10',
    15: 'bg-white/15',
    20: 'bg-white/20',
  }

  const baseClasses = `
    ${blurClasses[blur] || 'backdrop-blur-xl'}
    ${opacityClasses[opacity] || 'bg-white/10'}
    ${border ? 'border border-white/20' : ''}
    rounded-2xl
    shadow-lg shadow-black/10
  `

  const hoverClasses = hover ? `
    hover:bg-white/15
    hover:border-white/30
    hover:shadow-xl
    hover:shadow-black/20
    transition-all duration-300
  ` : ''

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 30,
      scale: 0.95,
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      transition: {
        duration: 0.5,
        delay,
        ease: [0.25, 0.46, 0.45, 0.94],
      }
    },
    hover: hover ? {
      y: -5,
      transition: {
        duration: 0.2,
        ease: 'easeOut',
      }
    } : {},
  }

  if (animate) {
    return (
      <motion.div
        className={`${baseClasses} ${hoverClasses} ${className}`}
        variants={cardVariants}
        initial="hidden"
        animate="visible"
        whileHover="hover"
        {...props}
      >
        {children}
      </motion.div>
    )
  }

  return (
    <div className={`${baseClasses} ${hoverClasses} ${className}`} {...props}>
      {children}
    </div>
  )
}

export default GlassCard
