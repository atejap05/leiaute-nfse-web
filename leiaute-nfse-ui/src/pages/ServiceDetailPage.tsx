import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Loader, AlertCircle, CheckCircle, XCircle } from 'lucide-react'
import api, { Servico, Regra } from '@/services/api'

export default function ServiceDetailPage() {
  const { codigo } = useParams<{ codigo: string }>()
  const [servico, setServico] = useState<Servico | null>(null)
  const [regras, setRegras] = useState<Regra[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      if (!codigo) return

      setLoading(true)
      setError(null)

      try {
        const numCodigo = parseInt(codigo, 10)
        const servicoData = await api.getServiceDetail(numCodigo)
        setServico(servicoData)

        const rulasData = await api.getServiceRules(numCodigo)
        setRegras(rulasData.regras)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Erro ao carregar serviço')
        setServico(null)
        setRegras([])
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [codigo])

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Loader className="w-8 h-8 text-primary-600 animate-spin" />
      </div>
    )
  }

  if (error || !servico) {
    return (
      <div className="space-y-4">
        <Link to="/" className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700">
          <ArrowLeft className="w-4 h-4" />
          Voltar
        </Link>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-red-800 dark:text-red-200">{error || 'Serviço não encontrado'}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Back Button */}
      <Link to="/" className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium">
        <ArrowLeft className="w-4 h-4" />
        Voltar para busca
      </Link>

      {/* Service Header */}
      <div className="card border-l-4 border-l-primary-600">
        <div className="mb-4">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            [{servico.codigo_tributacao}] {servico.descricao}
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Versão do leiaute: <span className="font-mono font-semibold">{servico.versao_leiaute}</span>
          </p>
        </div>

        {/* Localidade de Incidência */}
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <h2 className="font-semibold text-gray-900 dark:text-white mb-4">Localidade de Incidência (LC 116/03)</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center gap-3">
              {servico.estabelecimento_prestador ? (
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400 flex-shrink-0" />
              )}
              <span>Estabelecimento do Prestador</span>
            </div>
            <div className="flex items-center gap-3">
              {servico.local_prestacao ? (
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400 flex-shrink-0" />
              )}
              <span>Local de Prestação</span>
            </div>
            <div className="flex items-center gap-3">
              {servico.estabelecimento_tomador ? (
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400 flex-shrink-0" />
              )}
              <span>Estabelecimento do Tomador</span>
            </div>
            <div className="flex items-center gap-3">
              {servico.estabelecimento_emitente ? (
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
              ) : (
                <XCircle className="w-5 h-5 text-gray-400 flex-shrink-0" />
              )}
              <span>Estabelecimento Emitente</span>
            </div>
          </div>
        </div>

        {/* Grupos de Informação */}
        {(servico.obrigatorio || servico.info_complementares) && (
          <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
            <h2 className="font-semibold text-gray-900 dark:text-white mb-4">Grupos de Informação</h2>
            <div className="flex gap-4">
              {servico.obrigatorio && (
                <span className="badge badge-warning">Informações Obrigatórias</span>
              )}
              {servico.info_complementares && (
                <span className="badge badge-primary">Informações Complementares</span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Regras Aplicáveis */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Regras de Validação Aplicáveis ({regras.length})
        </h2>

        {regras.length === 0 ? (
          <div className="card text-center text-gray-600 dark:text-gray-400">
            Nenhuma regra específica para este serviço
          </div>
        ) : (
          <div className="space-y-3">
            {regras.map((regra) => (
              <div key={regra.id} className="card hover:shadow-lg transition">
                <div className="mb-2 flex items-start justify-between gap-4">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    Regra #{regra.numero_regra} - {regra.codigo_erro}
                  </h3>
                  <span className={`badge ${
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
                    <strong>Erro:</strong> {regra.mensagem_erro}
                  </p>
                </div>

                <p className="text-xs text-gray-600 dark:text-gray-400">
                  <strong>Campo:</strong> {regra.campo}
                  {regra.contexto && <> • <strong>Contexto:</strong> {regra.contexto}</>}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
