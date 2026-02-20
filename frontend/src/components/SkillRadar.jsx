import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts'

const defaultScores = {
  dsa: 0,
  backend: 0,
  communication: 0,
  projects: 0,
  systemDesign: 0,
}

const SkillRadar = ({ 
  scores = defaultScores,
  title = "Skill Analysis",
  showLegend = true,
  height = 350,
  fillColor = "#3b82f6",
  strokeColor = "#3b82f6",
}) => {
  const data = [
    { skill: 'DSA', value: scores.dsa || 0, fullMark: 100 },
    { skill: 'Backend', value: scores.backend || 0, fullMark: 100 },
    { skill: 'Communication', value: scores.communication || 0, fullMark: 100 },
    { skill: 'Projects', value: scores.projects || 0, fullMark: 100 },
    { skill: 'System Design', value: scores.systemDesign || 0, fullMark: 100 },
  ]

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 shadow-xl">
          <p className="text-white font-medium">{data.skill}</p>
          <p className="text-blue-400 text-sm">Score: {data.value}/100</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
          </svg>
          {title}
        </h3>
      )}
      
      <div style={{ height: height }} className="w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid 
              stroke="#475569" 
              strokeDasharray="3 3"
            />
            <PolarAngleAxis 
              dataKey="skill" 
              tick={{ 
                fill: '#94a3b8', 
                fontSize: 12,
                fontWeight: 500 
              }}
              tickLine={{ stroke: '#475569' }}
            />
            <PolarRadiusAxis 
              angle={90} 
              domain={[0, 100]} 
              tick={{ 
                fill: '#64748b', 
                fontSize: 10 
              }}
              tickCount={5}
              axisLine={{ stroke: '#475569' }}
            />
            <Radar
              name="Your Skills"
              dataKey="value"
              stroke={strokeColor}
              fill={fillColor}
              fillOpacity={0.3}
              strokeWidth={2}
              dot={{
                r: 4,
                fill: fillColor,
                strokeWidth: 2,
                stroke: '#1e293b'
              }}
              activeDot={{
                r: 6,
                fill: fillColor,
                stroke: '#fff',
                strokeWidth: 2
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  color: '#94a3b8' 
                }}
                formatter={(value) => (
                  <span className="text-slate-300 text-sm">{value}</span>
                )}
              />
            )}
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Score Summary */}
      <div className="mt-4 grid grid-cols-5 gap-2">
        {data.map((item) => {
          const getColor = (value) => {
            if (value >= 80) return 'text-green-400'
            if (value >= 60) return 'text-yellow-400'
            return 'text-red-400'
          }
          
          return (
            <div key={item.skill} className="text-center">
              <p className="text-slate-500 text-xs truncate">{item.skill}</p>
              <p className={`font-bold ${getColor(item.value)}`}>{item.value}</p>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default SkillRadar
