import { useState, useEffect } from 'react'
import { Loader, AlertCircle, Layers } from 'lucide-react'
import api, { Cenario } from '@/services/api'

export default function ScenariosPage() {
  const [cenarios, setCenarios] = useState<Cenario[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filtro, setFiltro] = useState<'todos' | 'brasil' | 'exportacao'>('todos')
  const [total, setTotal] = useState(0)

  useEffect(() => {
    const fetchCenarios = async () => {
      setLoading(true)
      setError(null)

      try {
        let data

        if (filtro === 'brasil') {
          data = await api.getDomesticScenarios(100)
          setCenarios(data.items)
          setTotal(data.cenarios_encontrados)
        } else if (filtro === 'exportacao') {
          data = await api.getExportScenarios(100)
          setCenarios(data.items)
          setTotal(data.cenarios_encontrados)
        } else {
          data = await api.getScenarios(100, 0)
          setCenarios(data.items)
          setTotal(data.total)
        }
      } catch (err: any) {
        setError(err.message || 'Erro ao carregar cenários')
        setCenarios([])
      } finally {
        setLoading(false)
      }
    }

    fetchCenarios()
  }, [filtro])

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Cenários de Exportação
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Total de <span className="font-bold text-primary-600">{total}</span> cenários
        </p>
      </div>

      {/* Filters */}
      <div className="card space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <Layers className="w-5 h-5 text-primary-600" />
          <h2 className="font-semibold text-gray-900 dark:text-white">Filtros</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => setFiltro('todos')}
            className={`px-4 py-3 rounded-lg font-medium transition ${
              filtro === 'todos'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            Todos os Cenários ({total})
          </button>
          <button
            onClick={() => setFiltro('brasil')}
            className={`px-4 py-3 rounded-lg font-medium transition ${
              filtro === 'brasil'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            🇧🇷 Brasil-Brasil
          </button>
          <button
            onClick={() => setFiltro('exportacao')}
            className={`px-4 py-3 rounded-lg font-medium transition ${
              filtro === 'exportacao'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            🌍 Exportação
          </button>
        </div>
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
      ) : cenarios.length === 0 ? (
        <div className="card text-center text-gray-600 dark:text-gray-400 py-12">
          Nenhum cenário encontrado
        </div>
      ) : (
        <div className="grid gap-4">
          {cenarios.map((cenario) => (
            <div key={cenario.id} className="card hover:shadow-lg transition">
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Cenário #{cenario.numero_cenario}
                </h3>
                <div className="flex gap-2 flex-wrap">
                  {cenario.obrigatorio_nbs && (
                    <span className="badge badge-warning text-xs">NBS Obrigatório</span>
                  )}
                  {cenario.obrigatorio_pais_resultado && (
                    <span className="badge badge-warning text-xs">País Resultado Obrigatório</span>
                  )}
                </div>
              </div>

              {/* Localidades */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
                <div>
                  <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-1">Tomador</p>
                  <p className="text-gray-900 dark:text-white font-medium">{cenario.endereco_tomador}</p>
                </div>
                <div>
                  <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-1">Local de Prestação</p>
                  <p className="text-gray-900 dark:text-white font-medium">{cenario.local_prestacao}</p>
                </div>
                <div>
                  <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-1">Intermediário</p>
                  <p className="text-gray-900 dark:text-white font-medium">{cenario.endereco_intermediario}</p>
                </div>
              </div>

              {/* Tributação */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-1">Tributação ISSQN</p>
                  <p className="text-gray-900 dark:text-white">
                    {cenario.tributacao_issqn || '-'}
                  </p>
                </div>
                <div>
                  <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-1">Imunidade/Não Incidência</p>
                  <p className="text-gray-900 dark:text-white">
                    {cenario.imunidade_exportacao || '-'}
                  </p>
                </div>
              </div>

              {/* Descrição */}
              {cenario.descricao && (
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <p className="text-sm text-gray-700 dark:text-gray-300">{cenario.descricao}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">ℹ️ Dica</h3>
        <p className="text-sm text-blue-800 dark:text-blue-300">
          Os cenários determinam a aplicação de regras de tributação (ISSQN), imunidade e obrigatoriedade de campos Comex (NBS e País Resultado) de acordo com as localidades do tomador, prestador e intermediário.
        </p>
      </div>
    </div>
  )
}
