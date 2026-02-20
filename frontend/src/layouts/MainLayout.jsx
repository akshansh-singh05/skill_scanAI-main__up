const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex flex-col">
      <header className="border-b border-slate-700 relative z-10">
        <nav className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-white">Your App</h1>
            <ul className="flex space-x-6">
              <li>
                <a href="/" className="text-slate-300 hover:text-white transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a href="/about" className="text-slate-300 hover:text-white transition-colors">
                  About
                </a>
              </li>
            </ul>
          </div>
        </nav>
      </header>
      <main className="flex-1 relative z-0">{children}</main>
      <footer className="border-t border-slate-700 relative z-10 bg-slate-900">
        <div className="container mx-auto px-4 py-6 text-center text-slate-400">
          <p>&copy; 2026 Your App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default MainLayout
