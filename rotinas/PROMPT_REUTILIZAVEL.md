# PROMPT REUTILIZÁVEL - CONVERSÃO DE LEIAUTE NFS-e

## INSTRUÇÕES PARA O USUÁRIO

1. Copie todo o conteúdo deste arquivo
2. Cole na conversa com a IA (Claude, ChatGPT, etc.)
3. Faça upload do arquivo Excel do novo leiaute
4. A IA seguirá o padrão estabelecido automaticamente

---

## PROMPT PARA A IA

```
Preciso converter o arquivo Excel do leiaute NFS-e que vou fazer upload para o formato padronizado que será usado em um portal web SPA.

IMPORTANTE: Siga EXATAMENTE a estrutura e padrão definidos abaixo para garantir compatibilidade com versões anteriores.

### ESTRUTURA DE SAÍDA OBRIGATÓRIA

Gere EXATAMENTE 10 arquivos seguindo este padrão:

#### 1. ARQUIVOS JSON (5 arquivos)

**Arquivo: 0_MASTER_INDEX.json**
```json
{
  "documento": "Sistema Nacional NFS-e - Documentação Técnica",
  "versao": "<extrair do nome do arquivo>",
  "data_conversao": "<ISO 8601>",
  "arquivo_origem": "<nome do arquivo>",
  "estatisticas": {
    "total_servicos": <número>,
    "total_cenarios_exportacao": <número>,
    "total_regras_recepcao": <número>,
    "total_campos_leiaute": <número>,
    "total_regras_validacao": <número>
  },
  "arquivos_gerados": [...]
}
```

**Arquivo: 1_servicos_incidencia.json**
```json
{
  "titulo": "Lista Nacional de Serviços - Incidência e Informações",
  "versao": "<versão>",
  "descricao": "Determinação da localidade de incidência (LI) de acordo com a LC 116/03",
  "total_servicos": <número>,
  "servicos": [
    {
      "codigo_tributacao": <número>,
      "descricao": "<texto>",
      "localidade_incidencia": {
        "estabelecimento_prestador": "X" ou null,
        "local_prestacao": "X" ou null,
        "estabelecimento_tomador": "X" ou null,
        "estabelecimento_emitente": "X" ou null
      },
      "grupos_informacao": {
        "obrigatorio": "X" ou "-" ou null,
        "info_complementares": "X" ou "-" ou null
      }
    }
  ]
}
```

**Arquivo: 2_cenarios_exportacao.json**
```json
{
  "titulo": "Cenários de Exportação para Emissão de NFS-e",
  "versao": "<versão>",
  "descricao": "Comportamento do sistema para validação de itens declarados pelo emitente",
  "total_cenarios": <número>,
  "cenarios": [
    {
      "cenario": <identificador>,
      "locais": {
        "endereco_tomador": "<valor>",
        "endereco_intermediario": "<valor>",
        "local_prestacao": "<valor>"
      },
      "subitem_lista": "<valor>",
      "local_incidencia_teorico": "<valor>",
      "tributacao": {
        "imunidade_exportacao_nao_incidencia": "<valor>",
        "tributacao_issqn": "<valor>"
      },
      "exportacao": {
        "issqn": "<valor>",
        "rfb": "<valor>"
      },
      "validacao": {
        "mensagem_erro_aviso": "<valor>",
        "local_incidencia_real": "<valor>"
      },
      "info_comex": {
        "nbs": "<valor>" ou null,
        "pais_resultado": "<valor>" ou null,
        "grupo_comex": "<valor>" ou null
      }
    }
  ]
}
```

**Arquivo: 3_regras_recepcao_dps.json**
```json
{
  "titulo": "Regras de Negócio para Recepção de DPS",
  "versao": "<versão>",
  "descricao": "Validações aplicadas na recepção de Declaração de Prestação de Serviço",
  "total_regras": <número>,
  "regras": [
    {
      "numero": <número>,
      "descricao": "<texto>",
      "aplicacao": "<valor>",
      "efeito": "<valor>",
      "codigo_erro": "<valor>",
      "mensagem_erro": "<texto>",
      "notas_explicativas": "<texto>"
    }
  ]
}
```

**Arquivo: 4_leiaute_dps_nfse.json**
```json
{
  "titulo": "Leiaute da DPS e NFS-e",
  "versao": "<versão>",
  "descricao": "Estrutura XML para Declaração de Prestação de Serviço e Nota Fiscal Eletrônica",
  "total_campos": <número>,
  "campos": [
    {
      "numero": <número>,
      "caminho_xml": "<caminho>",
      "campo": "<nome>",
      "elemento": "<tipo>",
      "tipo": "<tipo_dado>",
      "ocorrencia": "<padrão>",
      "tamanho": "<tamanho>",
      "descricao": "<texto>",
      "notas_explicativas": "<texto>"
    }
  ]
}
```

**Arquivo: 5_regras_validacao_nfse.json**
```json
{
  "titulo": "Regras de Negócio para DPS e NFS-e",
  "versao": "<versão>",
  "descricao": "Regras de validação aplicadas no Sistema Nacional NFS-e",
  "total_regras": <número>,
  "regras": [
    {
      "numero": <número>,
      "caminho_xml": "<caminho>",
      "campo": "<nome>",
      "regra_negocio": "<texto>",
      "aplicacao": "<valor>",
      "efeito": "<valor>",
      "codigo_erro": "<código>",
      "mensagem_erro": "<texto>",
      "nivel_regra": "<1|2|3>",
      "emissores_publicos": {
        "recepcao_dps": "<V|X>",
        "geracao_nfse_condicional": "<V|X>"
      },
      "adn_nfse": {
        "recepcao_compartilhada": "<V|X>",
        "recepcao_condicional": "<V|X>"
      },
      "observacoes": "<texto>"
    }
  ]
}
```

#### 2. ARQUIVOS MARKDOWN (5 arquivos)

**Arquivo: README.md**
- Visão geral da versão
- Arquivos disponíveis
- Exemplo de uso básico

**Arquivo: NFSE_DOCUMENTACAO_COMPLETA.md**
- Documentação técnica completa
- Explicação dos conceitos
- Referências

**Arquivo: GUIA_USO_AGENTES_IA.md**
- Instruções para uso por IA
- Exemplos de consultas
- Padrões de busca

**Arquivo: SUMARIO_CONVERSAO.md**
- Resumo da conversão
- Estatísticas
- Status

**Arquivo: VALIDACAO_SCHEMA.md** (novo)
- Schema de validação
- Testes de conformidade
- Checklist

### REGRAS CRÍTICAS

1. **Naming**: Mantenha EXATAMENTE os nomes dos arquivos
2. **Estrutura JSON**: Siga EXATAMENTE a estrutura definida
3. **Campos obrigatórios**: 
   - "titulo", "versao", "descricao", "total_*" 
   - Array principal com nome no plural
4. **Encoding**: UTF-8 em todos os arquivos
5. **Indentação JSON**: 2 espaços
6. **Valores null**: Use null (não string vazia) para campos não aplicáveis
7. **Tipos de dados**: 
   - Números como números (não strings)
   - Textos como strings
   - Booleanos como "X" ou null

### MAPEAMENTO DE ABAS DO EXCEL

**ABA 1** (nomes possíveis: "MUN.INCID_INFO.SERV.", "SERVICOS", "LISTA_SERVICOS")
→ 1_servicos_incidencia.json
- Linha inicial: 5
- Coluna código: 0
- Padrão: código_tributacao é numérico

**ABA 2** (nomes possíveis: "EXPORTACAO_EMISSÃO_NFS-e", "EXPORTACAO", "CENARIOS_EXPORTACAO")
→ 2_cenarios_exportacao.json
- Linha inicial: 6
- Identificar cenário por primeira coluna não vazia

**ABA 3** (nomes possíveis: "RN_RECEPCAO_DPS", "RECEPCAO_DPS", "REGRAS_RECEPCAO")
→ 3_regras_recepcao_dps.json
- Linha inicial: 2
- Número da regra na coluna 0

**ABA 4** (nomes possíveis: "LEIAUTE DPS_NFS-e", "LEIAUTE", "LEIAUTE_XML")
→ 4_leiaute_dps_nfse.json
- Linha inicial: 2
- Número sequencial na coluna 0

**ABA 5** (nomes possíveis: "RN DPS_NFS-e", "REGRAS_VALIDACAO", "RN_NFSE")
→ 5_regras_validacao_nfse.json
- Linha inicial: 4
- Número da regra na coluna 0

### EXTRAÇÃO DE VERSÃO

Do nome do arquivo: `anexovi-leiautesrn_rtc_ibscbs-v1-03-00-2013-nt007.xlsx`
Extrair: `v1-03-00-2013-nt007`

Padrão: buscar "v" seguido de números e hífens até encontrar ".xlsx"

### CHECKLIST DE VALIDAÇÃO

Antes de finalizar, verifique:

- [ ] 10 arquivos gerados
- [ ] 5 arquivos .json + 5 arquivos .md
- [ ] Todos os JSONs são válidos (sem erros de sintaxe)
- [ ] Encoding UTF-8 em todos
- [ ] Estrutura exata mantida
- [ ] Campos "versao" preenchidos
- [ ] Totais calculados corretamente
- [ ] Arrays nomeados no plural
- [ ] Campos null onde não há dados

### OUTPUT ESPERADO

Após processar, retorne:

1. Lista dos 10 arquivos gerados
2. Estatísticas (total de registros por arquivo)
3. Versão detectada
4. Confirmação de validação

### EXEMPLO DE RESPOSTA ESPERADA

```
✅ Conversão concluída com sucesso!

📦 Arquivos gerados:
  • 0_MASTER_INDEX.json
  • 1_servicos_incidencia.json (328 serviços)
  • 2_cenarios_exportacao.json (112 cenários)
  • 3_regras_recepcao_dps.json (16 regras)
  • 4_leiaute_dps_nfse.json (431 campos)
  • 5_regras_validacao_nfse.json (677 regras)
  • README.md
  • NFSE_DOCUMENTACAO_COMPLETA.md
  • GUIA_USO_AGENTES_IA.md
  • SUMARIO_CONVERSAO.md

📊 Estatísticas:
  Total de registros: 1.564
  Versão: v1-03-00-2013-nt007
  
✅ Validação: Todos os arquivos seguem o padrão estabelecido
```

### INÍCIO DO PROCESSAMENTO

Por favor, processe o arquivo Excel anexado seguindo RIGOROSAMENTE este padrão.
```

---

## NOTAS PARA O DESENVOLVEDOR

- Guarde este prompt em arquivo separado
- Use sempre o mesmo prompt para manter consistência
- Valide a saída comparando estrutura JSON com versões anteriores
- Mantenha versionamento dos arquivos gerados
