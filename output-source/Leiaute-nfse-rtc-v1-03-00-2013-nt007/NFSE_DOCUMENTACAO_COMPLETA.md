# Documentação Técnica - Sistema Nacional NFS-e

**Versão:** v1-03-00-2013-nt007  
**Fonte:** anexovi-leiautesrn_rtc_ibscbs-v1-03-00-2013-nt007.xlsx  
**Data de Conversão:** 2026-02-12

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Lista Nacional de Serviços](#lista-nacional-de-serviços)
3. [Cenários de Exportação](#cenários-de-exportação)
4. [Regras de Recepção DPS](#regras-de-recepção-dps)
5. [Leiaute XML DPS/NFS-e](#leiaute-xml-dpsnfs-e)
6. [Regras de Validação](#regras-de-validação)
7. [Referências de Arquivos](#referências-de-arquivos)

---

## Visão Geral

Este documento consolida a documentação técnica do Sistema Nacional de Nota Fiscal de Serviço Eletrônica (NFS-e), incluindo:

- **328 serviços** da Lista Nacional com regras de incidência do ISSQN
- **112 cenários** de exportação para emissão de NFS-e
- **16 regras** de validação para recepção de DPS
- **431 campos** de leiaute XML para DPS e NFS-e
- **677 regras** de negócio e validação

---

## Lista Nacional de Serviços

### Descrição
Determinação da Localidade de Incidência (LI) de acordo com a LC 116/03 e grupos de informações necessárias para detalhamento do serviço.

### Estrutura de Dados

Cada serviço contém:

- **Código de Tributação Nacional**: Código numérico único (ex: 10101)
- **Descrição do Serviço**: Texto descritivo do tipo de serviço
- **Localidade de Incidência (LI)**: Define onde o ISSQN incide
  - EP: Estabelecimento/Domicílio do Prestador
  - LP: Local da Prestação
  - ET: Estabelecimento/Domicílio do Tomador
  - EDEmit: Estabelecimento/Domicílio do Emitente (casos de importação)
- **Grupos de Informação**: Campos obrigatórios ou opcionais conforme o serviço

### Regras Gerais de Incidência

1. **Regra Geral**: Segue EP (Estabelecimento do Prestador) com exceções para LP (Local de Prestação) e ET (Estabelecimento do Tomador)

2. **Águas Marítimas**: 
   - Todos os serviços EXCETO 200101 podem ser prestados em "Águas Marítimas" (cLocPrestacao = 0000000)
   - Neste caso, LI será EDP (Estabelecimento do Prestador)

3. **Importação de Serviços**:
   - Quando Emitente = T (Tomador) ou I (Intermediário)
   - País Exterior em P (Prestador) e/ou LP (Local de Prestação)
   - A incidência do ISSQN em importação prevalece sobre regras do Art 3º da LC 116/03

### Arquivo de Dados
📄 `1_servicos_incidencia.json` - 328 serviços estruturados

---

## Cenários de Exportação

### Descrição
Define o comportamento do sistema para validação de itens declarados pelo emitente da DPS em casos de exportação de serviços.

### Elementos Declarados pelo Emitente

1. **Locais**:
   - Endereço do Tomador
   - Endereço do Intermediário
   - Local da Prestação do Serviço (LP)

2. **Tributação ISSQN**:
   - Subitem da Lista de Serviço
   - Resposta sobre: imunidade, exportação ou não incidência do ISSQN
   - Tributação do ISSQN e RFB

3. **Conceito de Comércio Exterior**:
   - Exportação para ISSQN (Local de Prestação no Exterior)
   - Exportação para RFB (ao menos 1 dos 3 locais no exterior)

### Comportamento do Sistema

Após validação, o sistema:
- Exibe mensagem de erro ou aviso se aplicável
- Define o Local de Incidência correto
- Determina obrigatoriedade de informações específicas:
  - **NBS** (Nomenclatura Brasileira de Serviços)
  - **País Resultado** (Exportação)
  - **Grupo Comex** (Comércio Exterior)

### Classificação de Preenchimento
- **SIM**: Obrigatório
- **NÃO**: Não permitido
- **Opcional**: Preenchimento opcional
- **X**: Cenário inexistente

### Arquivo de Dados
📄 `2_cenarios_exportacao.json` - 112 cenários estruturados

---

## Regras de Recepção DPS

### Descrição
Regras de negócio aplicadas na recepção da Declaração de Prestação de Serviço (DPS).

### Estrutura de Regras

Cada regra contém:
- **Número**: Identificador sequencial
- **Descrição**: Detalhamento da regra
- **Aplicação**: Nível de obrigatoriedade (Obrig., Opcional, etc.)
- **Efeito**: Consequência (Rej. = Rejeição, etc.)
- **Código de Erro**: Identificador do erro (ex: E1200)
- **Mensagem de Erro**: Texto apresentado ao usuário
- **Notas Explicativas**: Informações adicionais

### Principais Categorias de Validação

1. **Validação do Certificado de Transmissão**
   - Certificado de transmissor (existência, versão, validade)
   - Cadeia de certificação
   - Revogação de certificado

2. **Validação de Dados**
   - Estrutura do XML
   - Campos obrigatórios
   - Formatação e tipos de dados

3. **Validação de Negócio**
   - Regras específicas da legislação
   - Compatibilidade entre campos
   - Limites e restrições

### Arquivo de Dados
📄 `3_regras_recepcao_dps.json` - 16 regras estruturadas

---

## Leiaute XML DPS/NFS-e

### Descrição
Estrutura XML completa para Declaração de Prestação de Serviço (DPS) e Nota Fiscal de Serviço Eletrônica (NFS-e).

### Estrutura de Campos

Cada campo contém:
- **Número**: Ordem sequencial no leiaute
- **Caminho XML**: Localização no documento XML
- **Campo**: Nome do elemento/atributo
- **Elemento**: Tipo de elemento (Raiz, Grupo, Atributo, etc.)
- **Tipo**: Tipo de dados (C=Caracter, N=Numérico, D=Data, etc.)
- **Ocorrência**: Quantas vezes pode aparecer (ex: 1-1, 0-N)
- **Tamanho**: Tamanho máximo do campo
- **Descrição**: Detalhamento do campo
- **Notas Explicativas**: Informações complementares

### Principais Grupos de Informação

1. **Identificação da NFS-e**
   - Versão do leiaute
   - ID da NFS-e (53 posições)
   - Ambiente de geração

2. **Dados do Prestador**
   - Identificação (CPF/CNPJ)
   - Endereço
   - Inscrição Municipal

3. **Dados do Tomador**
   - Identificação
   - Endereço
   - Tipo de tomador

4. **Dados do Serviço**
   - Código de tributação
   - Discriminação
   - Valores e alíquotas
   - Local de prestação

5. **Informações Complementares**
   - Observações
   - Documentos referenciados
   - Informações específicas por tipo de serviço

### Arquivo de Dados
📄 `4_leiaute_dps_nfse.json` - 431 campos estruturados

---

## Regras de Validação

### Descrição
Regras de negócio completas para validação de DPS e NFS-e no Sistema Nacional.

### Níveis de Regras

- **Nível 1**: Regras de consistência do Leiaute NFS-e
- **Nível 2**: Regras gerais para todos os municípios aderentes ao SN NFS-e
- **Nível 3**: Regras específicas conforme legislação municipal parametrizada no SN NFS-e

### Aplicação das Regras

#### Emissores Públicos Nacionais (SEFIN, WEB, APP)
- **V**: Regra executada
- **X**: Regra não executada

Subdivisões:
1. Recepção de DPS enviadas pelo emitente prestador
2. Geração de informações de NFS-e pelos emissores públicos
3. NFS-e emitida sob condições de decisão judicial ou administrativa (cStat = 102)

#### ADN NFS-e (Ambiente de Dados Nacionais)
- **V**: Regra executada
- **X**: Regra não executada

Subdivisões:
1. Recepção de NFS-e compartilhadas pelos municípios
2. NFS-e emitidas sob condições de decisão judicial ou administrativa (cStat = 102)

### Estrutura de Regras

Cada regra contém:
- **Número**: Identificador sequencial
- **Caminho XML**: Campo específico sendo validado
- **Campo**: Nome do campo
- **Regra de Negócio**: Descrição da validação
- **Aplicação**: Nível de obrigatoriedade
- **Efeito**: Consequência (Rejeição, Aviso, etc.)
- **Código de Erro**: Identificador único do erro
- **Mensagem de Erro**: Texto apresentado ao usuário
- **Nível da Regra**: 1, 2 ou 3
- **Observações**: Informações adicionais

### Principais Categorias de Validação

1. **Versão e Estrutura**
   - Prazo de aceitação da versão do leiaute
   - Estrutura básica do XML

2. **Identificação**
   - Validação de CPF/CNPJ
   - Inscrições municipais
   - Códigos e identificadores

3. **Valores e Cálculos**
   - Valores de serviço
   - Deduções e descontos
   - Base de cálculo do ISSQN
   - Alíquotas aplicáveis

4. **Tributação**
   - Regime de tributação
   - Exigibilidade do ISSQN
   - Retenções e responsabilidades

5. **Localização**
   - Município de incidência
   - Local de prestação
   - Endereços de prestador e tomador

6. **Serviços**
   - Código de tributação nacional
   - Discriminação do serviço
   - Informações específicas por tipo de serviço

### Arquivo de Dados
📄 `5_regras_validacao_nfse.json` - 677 regras estruturadas

---

## Referências de Arquivos

### Arquivos JSON Gerados

Todos os arquivos estão em formato JSON com encoding UTF-8 para máxima compatibilidade com agentes de IA:

1. **1_servicos_incidencia.json**
   - Lista completa de serviços
   - Regras de incidência do ISSQN
   - Grupos de informação obrigatórios

2. **2_cenarios_exportacao.json**
   - Cenários de exportação
   - Validações de comércio exterior
   - Comportamento do sistema

3. **3_regras_recepcao_dps.json**
   - Regras de validação na recepção
   - Códigos e mensagens de erro
   - Certificados digitais

4. **4_leiaute_dps_nfse.json**
   - Estrutura completa do XML
   - Tipos de dados e tamanhos
   - Hierarquia de elementos

5. **5_regras_validacao_nfse.json**
   - Regras de negócio detalhadas
   - Níveis de aplicação
   - Contextos de execução

### Formato dos Dados

Todos os arquivos JSON seguem a estrutura:

```json
{
  "titulo": "Título descritivo",
  "descricao": "Descrição do conteúdo",
  "total_[tipo]": 123,
  "[tipo]": [
    {
      // dados estruturados
    }
  ]
}
```

### Uso Recomendado para Agentes de IA

1. **Consultas Específicas**: Use os arquivos JSON individuais para consultas focadas em um aspecto específico

2. **Visão Geral**: Use este documento Markdown para entender o contexto e as relações entre os diferentes componentes

3. **Validação de Dados**: Referencie os arquivos de regras (3 e 5) para implementar validações

4. **Geração de XML**: Use o arquivo 4 para estruturar corretamente documentos DPS/NFS-e

5. **Classificação de Serviços**: Use o arquivo 1 para identificar códigos de tributação e requisitos

---

## Glossário de Termos

- **ADN**: Ambiente de Dados Nacionais
- **DPS**: Declaração de Prestação de Serviço
- **EP**: Estabelecimento do Prestador
- **ET**: Estabelecimento do Tomador
- **ISSQN**: Imposto Sobre Serviços de Qualquer Natureza
- **LC 116/03**: Lei Complementar 116 de 2003
- **LI**: Localidade de Incidência
- **LP**: Local de Prestação
- **NBS**: Nomenclatura Brasileira de Serviços
- **NFS-e**: Nota Fiscal de Serviço Eletrônica
- **RFB**: Receita Federal do Brasil
- **SN**: Sistema Nacional

---

## Informações Adicionais

Para mais informações sobre a implementação técnica ou dúvidas específicas sobre as regras, consulte os arquivos JSON correspondentes ou a documentação oficial do Sistema Nacional NFS-e.

**Observação**: Este documento é uma conversão estruturada do arquivo Excel original e mantém a fidelidade às informações técnicas, reorganizadas para facilitar o consumo por agentes de IA e sistemas automatizados.
