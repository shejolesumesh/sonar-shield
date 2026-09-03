import { NavLink } from 'react-router-dom'

const links = [
  ['/', 'Dashboard'],
  ['/analysis', 'Sonar Analysis'],
  ['/priority', 'Recovery Priority'],
  ['/map', 'Map / Heatmap'],
  ['/review', 'Expert Review'],
  ['/reports', 'Reports'],
  ['/model', 'Model Info'],
]

export default function Layout({ children }) {
  return (
    <div className="min-h-screen">
      <header className="bg-abyss-800 border-b border-abyss-700 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-6 flex-wrap">
          <span className="text-xl font-bold text-sonar-400 tracking-wide">SONAR-SHIELD</span>
          <nav className="flex gap-1 flex-wrap text-sm">
            {links.map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `px-3 py-1.5 rounded ${isActive ? 'bg-sonar-500 text-abyss-900 font-semibold' : 'hover:bg-abyss-700'}`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
          <span className="ml-auto badge bg-yellow-900/50 text-yellow-300 border border-yellow-700">
            PROTOTYPE - DECISION SUPPORT ONLY
          </span>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
      <footer className="max-w-7xl mx-auto px-4 py-6 text-xs text-slate-500">
        SONAR-SHIELD prototype. Demo detector outputs are not scientifically validated.
        Risk scores are transparent prototype formulas, not validated environmental risk models.
      </footer>
    </div>
  )
}
