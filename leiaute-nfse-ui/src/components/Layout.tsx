import { Outlet, Link } from 'react-router-dom'
import { Search, BookOpen, Zap, Layers } from 'lucide-react'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition">
              <Zap className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">NFSe Leiaute</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">Portal de Consulta</p>
              </div>
            </Link>

            {/* Navigation */}
            <nav className="hidden sm:flex items-center gap-8">
              <Link to="/" className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition font-medium">
                <Search className="w-4 h-4" />
                Buscar
              </Link>
              <Link to="/rules" className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition font-medium">
                <BookOpen className="w-4 h-4" />
                Regras
              </Link>
              <Link to="/scenarios" className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition font-medium">
                <Layers className="w-4 h-4" />
                Cenários
              </Link>
            </nav>

            {/* API Status */}
            <div className="hidden md:flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-xs text-gray-600 dark:text-gray-400">API Online</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Sobre</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Portal de consulta do leiaute NFSe com 328 serviços e 677 regras de validação.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Recursos</h3>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><Link to="/" className="hover:text-primary-600 dark:hover:text-primary-400">Buscar Serviços</Link></li>
                <li><Link to="/rules" className="hover:text-primary-600 dark:hover:text-primary-400">Visualizar Regras</Link></li>
                <li><Link to="/scenarios" className="hover:text-primary-600 dark:hover:text-primary-400">Comparar Cenários</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Documentação</h3>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><a href="/api/docs" target="_blank" rel="noopener noreferrer" className="hover:text-primary-600 dark:hover:text-primary-400">API Swagger</a></li>
                <li><a href="#" className="hover:text-primary-600 dark:hover:text-primary-400">Guia do Leiaute</a></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-gray-300 dark:border-gray-700">
            <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
              © 2026 NFSe Portal • Dados baseados em especificações técnicas RFB/SEFAZ
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
