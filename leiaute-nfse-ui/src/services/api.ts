import axios, { AxiosInstance } from "axios";

// Types
export interface Servico {
  id: number;
  codigo_tributacao: number;
  descricao: string;
  estabelecimento_prestador?: string;
  local_prestacao?: string;
  estabelecimento_tomador?: string;
  estabelecimento_emitente?: string;
  obrigatorio?: string;
  info_complementares?: string;
  versao_leiaute: string;
}

export interface Regra {
  id: number;
  numero_regra: number;
  campo: string | null;
  regra_negocio: string | null;
  codigo_erro: string | null;
  mensagem_erro: string | null;
  nivel_regra: string | number | null;
  contexto: string | null;
  exemplay: string | null;
  versao_leiaute: string;
}

export interface Cenario {
  id: number;
  numero_cenario: number;
  endereco_tomador: string;
  endereco_intermediario: string;
  local_prestacao: string;
  imunidade_exportacao?: string;
  tributacao_issqn?: string;
  obrigatorio_nbs: boolean;
  obrigatorio_pais_resultado: boolean;
  descricao?: string;
  versao_leiaute: string;
}

export interface SearchResult {
  tipo: string;
  match_score: number;
  dados?: Record<string, any>;
  [key: string]: any;
}

export interface PaginatedResponse<T> {
  total: number;
  limit: number;
  offset: number;
  items: T[];
}

// API Client
class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: "/api",
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  // ============================================================================
  // Serviços
  // ============================================================================

  async getServices(
    limit: number = 10,
    offset: number = 0,
  ): Promise<PaginatedResponse<Servico>> {
    const response = await this.client.get("/services", {
      params: { limit, offset },
    });
    return response.data;
  }

  async getServiceDetail(codigo: number): Promise<Servico> {
    const response = await this.client.get(`/services/${codigo}`);
    return response.data;
  }

  async getServiceRules(
    codigo: number,
  ): Promise<{
    codigo_servico: number;
    total_regras: number;
    regras: Regra[];
  }> {
    const response = await this.client.get(`/services/${codigo}/rules`);
    return response.data;
  }

  // ============================================================================
  // Regras
  // ============================================================================

  async getRules(
    limit: number = 10,
    offset: number = 0,
    nivel?: number,
    codigo_erro?: string,
    campo?: string,
  ): Promise<PaginatedResponse<Regra>> {
    const response = await this.client.get("/rules", {
      params: {
        limit,
        offset,
        ...(nivel && { nivel }),
        ...(codigo_erro && { codigo_erro }),
        ...(campo && { campo }),
      },
    });
    return response.data;
  }

  async getRuleDetail(numero: number): Promise<Regra> {
    const response = await this.client.get(`/rules/${numero}`);
    return response.data;
  }

  async getRulesByLevel(
    nivel: number,
    limit: number = 20,
  ): Promise<{ nivel: number; total: number; items: Regra[] }> {
    const response = await this.client.get(`/rules/filtro/por-nivel/${nivel}`, {
      params: { limit },
    });
    return response.data;
  }

  async getRulesByErrorCode(
    codigo_erro: string,
  ): Promise<{ codigo_erro: string; total: number; items: Regra[] }> {
    const response = await this.client.get(
      `/rules/filtro/por-erro/${codigo_erro}`,
    );
    return response.data;
  }

  // ============================================================================
  // Cenários
  // ============================================================================

  async getScenarios(
    limit: number = 10,
    offset: number = 0,
    endereco_tomador?: string,
    local_prestacao?: string,
  ): Promise<PaginatedResponse<Cenario>> {
    const response = await this.client.get("/scenarios", {
      params: {
        limit,
        offset,
        ...(endereco_tomador && { endereco_tomador }),
        ...(local_prestacao && { local_prestacao }),
      },
    });
    return response.data;
  }

  async getScenarioDetail(numero: number): Promise<Cenario> {
    const response = await this.client.get(`/scenarios/${numero}`);
    return response.data;
  }

  async compareScenarios(
    ids: number[],
  ): Promise<{
    cenarios_comparados: number;
    cenarios: Cenario[];
    diferencas: any;
  }> {
    const params = new URLSearchParams();
    ids.forEach(id => params.append("cenarios_ids", id.toString()));

    const response = await this.client.post("/scenarios/compare", null, {
      params,
    });
    return response.data;
  }

  async getDomesticScenarios(
    limit: number = 10,
  ): Promise<{ cenarios_encontrados: number; items: Cenario[] }> {
    const response = await this.client.get("/scenarios/filtro/brasil-brasil", {
      params: { limit },
    });
    return response.data;
  }

  async getExportScenarios(
    limit: number = 10,
  ): Promise<{ cenarios_encontrados: number; items: Cenario[] }> {
    const response = await this.client.get("/scenarios/filtro/exportacao", {
      params: { limit },
    });
    return response.data;
  }

  // ============================================================================
  // Busca
  // ============================================================================

  async search(
    q: string,
    tipo?: string,
    limit: number = 20,
  ): Promise<{
    query: string;
    filtro_tipo: string | null;
    total_resultados: number;
    items: SearchResult[];
  }> {
    const response = await this.client.get("/search", {
      params: {
        q,
        ...(tipo && { tipo }),
        limit,
      },
    });
    const raw = response.data ?? {};
    const resultados: SearchResult[] = Array.isArray(raw.resultados)
      ? raw.resultados
      : Array.isArray(raw.items)
        ? raw.items
        : [];

    const items = resultados.map((r) => {
      const dados = r?.dados && typeof r.dados === "object" ? r.dados : {};
      // Compatibilidade com UI atual: mantém campos em raiz e preserva "dados"
      return { ...dados, ...r, dados };
    });

    return {
      query: raw.query ?? q,
      filtro_tipo: raw.filtro_tipo ?? null,
      total_resultados: raw.total_resultados ?? items.length,
      items,
    };
  }

  async searchByServiceCode(
    codigo: number,
  ): Promise<{ encontrado: boolean; servico?: any }> {
    const response = await this.client.get(`/search/codigo/${codigo}`);
    return response.data;
  }

  async searchByErrorCode(
    codigo_erro: string,
  ): Promise<{
    encontrado: boolean;
    codigo_erro: string;
    total: number;
    regras: any[];
  }> {
    const response = await this.client.get(`/search/erro/${codigo_erro}`);
    return response.data;
  }

  // ============================================================================
  // Health
  // ============================================================================

  async health(): Promise<{ status: string }> {
    const response = await this.client.get("/health");
    return response.data;
  }
}

export default new APIClient();
