const Card = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`bg-slate-800 rounded-xl p-6 border border-slate-700 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
