import { useState, useEffect } from 'react'
import { Loader, AlertCircle, Filter } from 'lucide-react'
import api, { Regra } from '@/services/api'

export default function RulesPage() {
  const [regras, setRegras] = useState<Regra[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [nivel, setNivel] = useState<number | undefined>(undefined)
  const [campo, setCampo] = useState('')
  const [offset, setOffset] = useState(0)
  const [total, setTotal] = useState(0)

  const limit = 20

  useEffect(() => {
    const fetchRegras = async () => {
      setLoading(true)
      setError(null)

      try {
        const data = await api.getRules(limit, offset, nivel, undefined, campo || undefined)
        setRegras(data.items)
        setTotal(data.total)
      } catch (err: any) {
        setError(err.message || 'Erro ao carregar regras')
        setRegras([])
      } finally {
        setLoading(false)
      }
    }

    fetchRegras()
  }, [nivel, campo, offset])

  const handleNivelChange = (newNivel: number | undefined) => {
    setNivel(newNivel)
    setOffset(0)
  }

  const handleCampoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCampo(e.target.value)
    setOffset(0)
  }

  const currentPage = Math.floor(offset / limit) + 1
  const totalPages = Math.ceil(total / limit)

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Regras de Validação NFSe
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Total de <span className="font-bold text-primary-600">{total}</span> regras de negócio
        </p>
      </div>

      {/* Filters */}
      <div className="card space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <Filter className="w-5 h-5 text-primary-600" />
          <h2 className="font-semibold text-gray-900 dark:text-white">Filtros</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Nível Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nível de Regra
            </label>
            <select
              value={nivel ?? ''}
              onChange={(e) => handleNivelChange(e.target.value ? parseInt(e.target.value) : undefined)}
              className="w-full text-sm px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
            >
              <option value="">Todos os níveis</option>
              <option value="1">Nível 1 (Leiaute)</option>
              <option value="2">Nível 2 (Regras Gerais)</option>
              <option value="3">Nível 3 (Regras Municipais)</option>
            </select>
          </div>

          {/* Campo Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Filtrar por Campo
            </label>
            <input
              type="text"
              placeholder="Digite o nome do campo..."
              value={campo}
              onChange={handleCampoChange}
              className="w-full input-base text-sm"
            />
          </div>
        </div>

        {/* Clear Filters */}
        {(nivel || campo) && (
          <button
            onClick={() => {
              setNivel(undefined)
              setCampo('')
              setOffset(0)
            }}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Limpar filtros
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading ? (
        <div className="flex justify-center items-center min-h-[300px]">
          <Loader className="w-8 h-8 text-primary-600 animate-spin" />
        </div>
      ) : regras.length === 0 ? (
        <div className="card text-center text-gray-600 dark:text-gray-400 py-12">
          Nenhuma regra encontrada com os filtros aplicados
        </div>
      ) : (
        <>
          {/* Results */}
          <div className="space-y-3">
            {regras.map((regra) => (
              <div key={regra.id} className="card hover:shadow-lg transition">
                <div className="flex items-start justify-between gap-4 mb-2">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      Regra #{regra.numero_regra} - {regra.codigo_erro}
                    </h3>
                  </div>
                  <span className={`badge text-nowrap ${
                    regra.nivel_regra === 1 ? 'badge-error' :
                    regra.nivel_regra === 2 ? 'badge-warning' :
                    'badge-primary'
                  }`}>
                    Nível {regra.nivel_regra}
                  </span>
                </div>

                <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">{regra.regra_negocio}</p>

                <div className="bg-gray-50 dark:bg-gray-700 rounded p-3 border border-gray-200 dark:border-gray-600 mb-3">
                  <p className="text-sm font-mono text-gray-700 dark:text-gray-300">
                    <strong>Mensagem:</strong> {regra.mensagem_erro}
                  </p>
                </div>

                <div className="flex flex-wrap gap-2 text-xs text-gray-600 dark:text-gray-400">
                  <span>
                    <strong>Campo:</strong> {regra.campo}
                  </span>
                  {regra.contexto && (
                    <span>
                      <strong>Contexto:</strong> {regra.contexto}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Exibindo {offset + 1} a {Math.min(offset + limit, total)} de {total} regras
            </p>

            <div className="flex gap-2">
              <button
                onClick={() => setOffset(Math.max(0, offset - limit))}
                disabled={offset === 0}
                className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700 transition"
              >
                Anterior
              </button>
              <div className="flex items-center gap-2 px-4 py-2">
                <span className="text-sm font-medium">
                  {currentPage} de {totalPages}
                </span>
              </div>
              <button
                onClick={() => setOffset(offset + limit)}
                disabled={offset + limit >= total}
                className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700 transition"
              >
                Próximo
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
