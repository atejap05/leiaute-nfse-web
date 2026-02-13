# Guia de Uso - Documentação NFS-e para Agentes de IA

## Como Usar Esta Documentação

Este guia fornece instruções específicas para agentes de IA sobre como consultar e utilizar a documentação técnica do Sistema Nacional NFS-e.

---

## Estrutura dos Arquivos

### 1. Documento Principal (Markdown)
📄 **NFSE_DOCUMENTACAO_COMPLETA.md**
- Visão geral e contexto
- Explicação de conceitos
- Índice navegável
- Glossário de termos

### 2. Dados Estruturados (JSON)
Os arquivos JSON contêm dados estruturados prontos para processamento:

```
1_servicos_incidencia.json      → 328 serviços
2_cenarios_exportacao.json      → 112 cenários
3_regras_recepcao_dps.json      → 16 regras de recepção
4_leiaute_dps_nfse.json         → 431 campos XML
5_regras_validacao_nfse.json    → 677 regras de validação
```

---

## Casos de Uso Comuns

### 1. Identificar Código de Tributação de um Serviço

**Pergunta típica**: "Qual o código de tributação para desenvolvimento de software?"

**Passos**:
1. Carregar `1_servicos_incidencia.json`
2. Buscar na descrição dos serviços
3. Retornar código e regras de incidência

**Exemplo de resposta**:
```json
{
  "codigo_tributacao": 10101,
  "descricao": "Análise e desenvolvimento de sistemas.",
  "localidade_incidencia": {
    "estabelecimento_prestador": "X",
    "estabelecimento_emitente": "X"
  }
}
```

---

### 2. Validar Local de Incidência do ISSQN

**Pergunta típica**: "Para o serviço 10101, onde incide o ISSQN?"

**Passos**:
1. Buscar o serviço em `1_servicos_incidencia.json`
2. Verificar campo `localidade_incidencia`
3. Explicar onde incidem os tributos

**Interpretação dos marcadores**:
- **X** = Aplica-se esta regra
- **-** = Não aplica esta regra
- **null** = Não informado

---

### 3. Verificar Cenário de Exportação

**Pergunta típica**: "Como tratar um serviço prestado para o exterior?"

**Passos**:
1. Carregar `2_cenarios_exportacao.json`
2. Identificar características do cenário:
   - Localização do tomador
   - Localização do intermediário
   - Local de prestação
3. Encontrar cenário correspondente
4. Retornar regras de tributação e obrigatoriedade de campos

**Campos de obrigatoriedade**:
- **SIM** = Obrigatório
- **NÃO** = Não permitido
- **Opcional** = Preenchimento opcional
- **X** = Cenário inexistente

---

### 4. Validar Estrutura de XML

**Pergunta típica**: "Quais campos são obrigatórios na NFS-e?"

**Passos**:
1. Carregar `4_leiaute_dps_nfse.json`
2. Filtrar por `ocorrencia` que contém "1-1" (obrigatório)
3. Listar campos e suas características

**Interpretação de ocorrência**:
- **1-1** = Obrigatório (1 vez)
- **0-1** = Opcional (0 ou 1 vez)
- **1-N** = Obrigatório (1 ou mais vezes)
- **0-N** = Opcional (0 ou mais vezes)

---

### 5. Consultar Regras de Validação

**Pergunta típica**: "Quais validações são aplicadas ao campo CPF do prestador?"

**Passos**:
1. Carregar `5_regras_validacao_nfse.json`
2. Buscar por `caminho_xml` ou `campo` contendo "CPF" ou "prestador"
3. Retornar regras aplicáveis com códigos de erro

**Níveis de regras**:
- **Nível 1** = Consistência de leiaute
- **Nível 2** = Regras gerais para todos os municípios
- **Nível 3** = Regras específicas municipais

---

## Padrões de Consulta

### Busca por Código

```python
# Exemplo: Buscar serviço por código
def buscar_servico(codigo):
    servicos = carregar_json('1_servicos_incidencia.json')
    for servico in servicos['servicos']:
        if servico['codigo_tributacao'] == codigo:
            return servico
    return None
```

### Busca por Descrição

```python
# Exemplo: Buscar serviço por palavra-chave
def buscar_por_palavra(palavra):
    servicos = carregar_json('1_servicos_incidencia.json')
    resultados = []
    for servico in servicos['servicos']:
        if palavra.lower() in servico['descricao'].lower():
            resultados.append(servico)
    return resultados
```

### Busca por Caminho XML

```python
# Exemplo: Buscar campo do leiaute
def buscar_campo_xml(caminho):
    leiaute = carregar_json('4_leiaute_dps_nfse.json')
    for campo in leiaute['campos']:
        if caminho in campo['caminho_xml']:
            return campo
    return None
```

---

## Interpretação de Campos Especiais

### Localidade de Incidência

```json
"localidade_incidencia": {
  "estabelecimento_prestador": "X",      // EP - onde está o prestador
  "local_prestacao": null,               // LP - onde o serviço é prestado
  "estabelecimento_tomador": null,       // ET - onde está o tomador
  "estabelecimento_emitente": "X"        // EDEmit - quem emite (importação)
}
```

**Lógica de aplicação**:
1. Verificar se há importação (EDEmit = "X")
2. Se não, seguir ordem: EP → LP → ET
3. O primeiro com "X" define a incidência

### Tipos de Dados no Leiaute

- **C** = Caracter (texto)
- **N** = Numérico (números)
- **D** = Data
- **H** = Hora
- **A** = Atributo XML
- **G** = Grupo de elementos
- **E** = Elemento XML

### Códigos de Erro

Formato: **EXXXX**
- **E1XXX** = Erros de estrutura/formato
- **E2XXX** = Erros de validação de negócio
- **E3XXX** = Erros de autenticação/autorização

---

## Fluxos de Validação Recomendados

### Validação de DPS (Declaração)

1. **Estrutura XML** → `4_leiaute_dps_nfse.json`
   - Verificar campos obrigatórios
   - Validar tipos de dados
   - Confirmar hierarquia

2. **Regras de Recepção** → `3_regras_recepcao_dps.json`
   - Certificado digital
   - Assinatura
   - Versão do leiaute

3. **Regras de Negócio** → `5_regras_validacao_nfse.json`
   - Valores e cálculos
   - Códigos de serviço
   - Tributação

### Validação de Exportação

1. **Identificar Localidades** → `2_cenarios_exportacao.json`
   - Endereço do tomador
   - Endereço do intermediário
   - Local de prestação

2. **Encontrar Cenário Correspondente**
   - Combinar localidades
   - Verificar subitem da lista

3. **Aplicar Regras**
   - Tributação ISSQN
   - Obrigatoriedade de campos NBS, País, Comex
   - Mensagens de validação

---

## Exemplos de Queries Complexas

### 1. Listar Todos os Serviços com Incidência no Local de Prestação

```python
servicos_lp = [
    s for s in servicos['servicos']
    if s['localidade_incidencia']['local_prestacao'] == 'X'
]
```

### 2. Encontrar Regras de Nível 3 (Municipais)

```python
regras_municipais = [
    r for r in regras['regras']
    if r['nivel_regra'] == '3'
]
```

### 3. Campos Obrigatórios de um Grupo Específico

```python
campos_obrigatorios = [
    c for c in leiaute['campos']
    if 'prestador' in c['caminho_xml'].lower()
    and '1-1' in c['ocorrencia']
]
```

### 4. Erros que Causam Rejeição

```python
erros_rejeicao = [
    r for r in regras['regras']
    if r['efeito'] == 'Rej.'
]
```

---

## Dicas para Agentes de IA

### 1. Contexto é Fundamental
Sempre considere o contexto completo:
- Tipo de serviço
- Localização (prestador, tomador, local de prestação)
- Regime tributário
- Cenário de exportação (se aplicável)

### 2. Priorização de Regras
Em caso de conflito, a ordem de priorização é:
1. Regras de importação/exportação
2. Regras de nível 3 (municipais)
3. Regras de nível 2 (nacionais)
4. Regras de nível 1 (estrutura)

### 3. Validação Progressiva
Valide em camadas:
1. Estrutura XML (leiaute)
2. Certificados e assinaturas
3. Dados obrigatórios
4. Regras de negócio
5. Cálculos e valores

### 4. Mensagens Claras
Ao reportar erros:
- Use o código de erro oficial (EXXXX)
- Inclua a mensagem padrão
- Adicione contexto específico
- Sugira correção quando possível

### 5. Tratamento de Exceções
Sempre considere casos especiais:
- Águas marítimas (código 0000000)
- Decisões judiciais (cStat = 102)
- Importação de serviços
- Múltiplos municípios envolvidos

---

## Checklist de Validação Completa

### Para DPS (Declaração de Prestação de Serviço)

- [ ] XML bem formado
- [ ] Versão do leiaute válida
- [ ] Certificado digital válido
- [ ] Assinatura válida
- [ ] Campos obrigatórios preenchidos
- [ ] Tipos de dados corretos
- [ ] CPF/CNPJ válidos
- [ ] Código de serviço existe na lista nacional
- [ ] Local de incidência correto
- [ ] Valores e cálculos consistentes
- [ ] Alíquota aplicável correta
- [ ] Informações específicas do serviço presentes
- [ ] Se exportação: campos Comex preenchidos
- [ ] Regras municipais atendidas

### Para NFS-e (Nota Fiscal)

- [ ] Todos os itens da DPS, mais:
- [ ] Número da NFS-e válido e único
- [ ] Data de emissão válida
- [ ] Código de verificação gerado
- [ ] Status de processamento correto
- [ ] Dados do emitente completos
- [ ] Compartilhamento com ADN (se aplicável)

---

## Glossário de Ações

Quando o usuário solicitar:

- **"Validar"** → Aplicar todas as regras relevantes e retornar erros/avisos
- **"Consultar"** → Buscar informação sem aplicar regras
- **"Gerar"** → Criar estrutura XML baseada nas especificações
- **"Classificar"** → Identificar código de tributação adequado
- **"Calcular"** → Determinar valores de ISSQN, deduções, etc.
- **"Verificar"** → Confirmar conformidade com regras específicas

---

## Atualizações e Manutenção

Esta documentação é baseada na versão **v1-03-00-2013-nt007** da especificação NFS-e.

Para verificar se há atualizações:
1. Consultar site oficial do Sistema Nacional NFS-e
2. Comparar versões de leiaute
3. Revisar notas técnicas mais recentes

---

## Suporte e Referências

- Documentação original: arquivo Excel fornecido
- Sistema Nacional NFS-e: www.nfse.gov.br (verificar URL oficial)
- Lei Complementar 116/2003
- Portarias e Instruções Normativas relacionadas

---

**Última Atualização**: 2026-02-12  
**Versão do Documento**: 1.0
