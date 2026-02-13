import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Search as SearchIcon, Loader, AlertCircle } from 'lucide-react'
import api, { SearchResult, Servico } from '@/services/api'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (query.trim().length < 2) {
      setError('Digite pelo menos 2 caracteres')
      return
    }

    setLoading(true)
    setError(null)
    setHasSearched(true)

    try {
      const data = await api.search(query.trim(), undefined, 30)
      setResults(data.items)
      
      if (data.items.length === 0) {
        setError('Nenhum resultado encontrado')
      }
    } catch (err: any) {
      setError(err.message || 'Erro ao buscar. Tente novamente.')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const groupedResults = useMemo(() => {
    const groups: { [key: string]: SearchResult[] } = {}
    results.forEach(result => {
      if (!groups[result.tipo]) {
        groups[result.tipo] = []
      }
      groups[result.tipo].push(result)
    })
    return groups
  }, [results])

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Buscar no Leiaute NFSe
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Encontre serviços, regras de validação e campos do leiaute
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
        <div className="relative">
          <input
            type="text"
            placeholder="Digite uma descrição de serviço, código de erro ou número de regra..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-primary-600 focus:outline-none dark:bg-gray-800 dark:border-gray-600 dark:text-white"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition"
          >
            <SearchIcon className="w-6 h-6 text-gray-400" />
          </button>
        </div>
      </form>

      {/* Error Message */}
      {error && hasSearched && (
        <div className="max-w-2xl mx-auto bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex gap-3 items-start">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex justify-center">
          <Loader className="w-8 h-8 text-primary-600 animate-spin" />
        </div>
      )}

      {/* Results */}
      {hasSearched && !loading && results.length > 0 && (
        <div className="space-y-6">
          <p className="text-center text-gray-600 dark:text-gray-400">
            Encontrados <span className="font-bold text-primary-600">{results.length}</span> resultados
          </p>

          {/* Results by Type */}
          {Object.entries(groupedResults).map(([tipo, items]) => (
            <div key={tipo} className="space-y-3">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white capitalize">
                {tipo === 'servico' && '🏢 Serviços'}
                {tipo === 'regra' && '⚖️ Regras'}
                {tipo === 'campo' && '📋 Campos'}
              </h2>

              <div className="grid gap-3">
                {items.slice(0, 10).map((item, idx) => (
                  <div key={idx} className="card hover:shadow-lg transition">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        {item.tipo === 'servico' && (
                          <Link to={`/services/${item.codigo}`} className="hover:text-primary-600 dark:hover:text-primary-400">
                            <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                              [{item.codigo}] {item.descricao}
                            </h3>
                          </Link>
                        )}
                        {item.tipo === 'regra' && (
                          <>
                            <h3 className="font-semibold text-gray-900 dark:text-white">
                              Regra #{item.numero} - {item.codigo_erro}
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{item.descricao}</p>
                            <div className="flex gap-2 mt-2 flex-wrap">
                              <span className="badge badge-primary">Campo: {item.campo}</span>
                              <span className="badge badge-secondary">Nível {item.nivel}</span>
                            </div>
                          </>
                        )}
                        {item.tipo === 'campo' && (
                          <>
                            <h3 className="font-semibold text-gray-900 dark:text-white">
                              {item.nome} ({item.elemento_xml})
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{item.descricao}</p>
                            <div className="flex gap-2 mt-2 flex-wrap">
                              <span className="badge badge-primary">{item.tipo_dado}</span>
                              <span className="badge badge-secondary">{item.ocorrencia}</span>
                            </div>
                          </>
                        )}
                      </div>
                      <div className="flex-shrink-0">
                        <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-primary-100 dark:bg-primary-900">
                          <span className="text-sm font-bold text-primary-600 dark:text-primary-400">
                            {(item.match_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {items.length > 10 && (
                <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
                  ... e mais {items.length - 10} resultados de {tipo}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!hasSearched && (
        <div className="max-w-2xl mx-auto text-center py-12">
          <SearchIcon className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Digite um termo de busca para começar
          </p>
        </div>
      )}
    </div>
  )
}
