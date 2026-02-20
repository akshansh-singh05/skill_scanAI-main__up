import { useState, useEffect } from 'react'

/**
 * CompanySelector - Select interview mode based on target company
 * 
 * Features:
 * - Visual company cards with logos
 * - Focus areas and interview style info
 * - Tips for each company's interview process
 */
const CompanySelector = ({ onSelect, selectedCompany = null }) => {
  const [companies, setCompanies] = useState([])
  const [selected, setSelected] = useState(selectedCompany)
  const [loading, setLoading] = useState(true)
  const [showDetails, setShowDetails] = useState(null)

  // Fallback company data in case API fails
  const fallbackCompanies = [
    {
      id: "google",
      name: "Google",
      logo: "🔍",
      color: "#4285F4",
      tagline: "Think Big, Code Smart",
      description: "Heavy focus on Data Structures & Algorithms, optimization, and scalability",
      focus_areas: ["DSA", "Problem Solving", "System Design", "Googleyness"],
    },
    {
      id: "amazon",
      name: "Amazon",
      logo: "📦",
      color: "#FF9900",
      tagline: "Leadership Principles First",
      description: "Strong emphasis on Amazon's 16 Leadership Principles with STAR method responses",
      focus_areas: ["Leadership Principles", "Behavioral", "System Design", "Coding"],
    },
    {
      id: "meta",
      name: "Meta",
      logo: "♾️",
      color: "#0668E1",
      tagline: "Move Fast, Build Things",
      description: "Balance of coding excellence and system design with focus on scale",
      focus_areas: ["Coding", "System Design", "Product Sense", "Behavioral"],
    },
    {
      id: "microsoft",
      name: "Microsoft",
      logo: "🪟",
      color: "#00A4EF",
      tagline: "Empower Every Person",
      description: "Balanced approach with focus on growth mindset and collaboration",
      focus_areas: ["Coding", "System Design", "Problem Solving", "Growth Mindset"],
    },
    {
      id: "apple",
      name: "Apple",
      logo: "🍎",
      color: "#555555",
      tagline: "Think Different",
      description: "Deep technical expertise with focus on quality and user experience",
      focus_areas: ["Technical Excellence", "Design Thinking", "Attention to Detail", "Innovation"],
    },
    {
      id: "generic",
      name: "General Practice",
      logo: "💼",
      color: "#6366F1",
      tagline: "All-Round Preparation",
      description: "Balanced preparation covering all major interview topics",
      focus_areas: ["DSA", "System Design", "Behavioral", "Coding"],
    },
  ]

  useEffect(() => {
    fetchCompanies()
  }, [])

  const fetchCompanies = async () => {
    try {
      const response = await fetch('/api/interview/companies')
      if (response.ok) {
        const data = await response.json()
        setCompanies(data.companies || fallbackCompanies)
      } else {
        setCompanies(fallbackCompanies)
      }
    } catch (err) {
      console.error('Failed to fetch companies:', err)
      setCompanies(fallbackCompanies)
    } finally {
      setLoading(false)
    }
  }

  const handleSelect = (company) => {
    setSelected(company.id)
    onSelect?.(company)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin w-8 h-8 border-3 border-blue-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h3 className="text-xl font-bold text-white mb-2">
          Select Interview Mode
        </h3>
        <p className="text-slate-400">
          Choose a company to practice their specific interview style
        </p>
      </div>

      {/* Company Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {companies.map((company) => (
          <button
            key={company.id}
            onClick={() => handleSelect(company)}
            onMouseEnter={() => setShowDetails(company.id)}
            onMouseLeave={() => setShowDetails(null)}
            className={`
              relative p-4 rounded-xl border-2 transition-all duration-200
              ${selected === company.id
                ? 'border-blue-500 bg-blue-500/10 scale-[1.02]'
                : 'border-slate-700 bg-slate-800/50 hover:border-slate-500 hover:bg-slate-800'
              }
            `}
          >
            {/* Selected indicator */}
            {selected === company.id && (
              <div className="absolute top-2 right-2">
                <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
            )}

            {/* Company Logo */}
            <div 
              className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-3 mx-auto"
              style={{ backgroundColor: `${company.color}20` }}
            >
              {company.logo}
            </div>

            {/* Company Name */}
            <h4 className="text-white font-semibold text-center">
              {company.name}
            </h4>

            {/* Tagline */}
            <p className="text-xs text-slate-500 text-center mt-1">
              {company.tagline}
            </p>

            {/* Hover Details */}
            {showDetails === company.id && (
              <div className="absolute left-0 right-0 top-full mt-2 p-3 rounded-lg bg-slate-900 border border-slate-700 shadow-xl z-10 text-left">
                <p className="text-xs text-slate-300 mb-2">{company.description}</p>
                <div className="flex flex-wrap gap-1">
                  {company.focus_areas?.slice(0, 3).map((area, idx) => (
                    <span 
                      key={idx}
                      className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300"
                    >
                      {area}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </button>
        ))}
      </div>

      {/* Selected Company Details */}
      {selected && (
        <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700 animate-fadeIn">
          {(() => {
            const company = companies.find(c => c.id === selected)
            if (!company) return null

            return (
              <>
                <div className="flex items-center gap-3 mb-4">
                  <div 
                    className="w-10 h-10 rounded-lg flex items-center justify-center text-xl"
                    style={{ backgroundColor: `${company.color}20` }}
                  >
                    {company.logo}
                  </div>
                  <div>
                    <h4 className="text-white font-semibold">{company.name} Mode</h4>
                    <p className="text-sm text-slate-400">{company.tagline}</p>
                  </div>
                </div>

                <p className="text-sm text-slate-300 mb-4">{company.description}</p>

                <div className="space-y-3">
                  <div>
                    <h5 className="text-xs font-medium text-slate-400 uppercase tracking-wide mb-2">
                      Focus Areas
                    </h5>
                    <div className="flex flex-wrap gap-2">
                      {company.focus_areas?.map((area, idx) => (
                        <span 
                          key={idx}
                          className="text-sm px-3 py-1 rounded-lg text-white"
                          style={{ backgroundColor: `${company.color}30`, borderColor: company.color }}
                        >
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </>
            )
          })()}
        </div>
      )}

      {/* Style */}
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  )
}

export default CompanySelector
