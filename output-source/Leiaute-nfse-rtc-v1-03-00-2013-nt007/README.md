# Documentação NFS-e - Formato Otimizado para IA

## 📋 Visão Geral

Esta documentação foi convertida do formato Excel original para formatos estruturados (JSON e Markdown) otimizados para consumo por agentes de IA e sistemas automatizados.

**Arquivo Original**: `anexovi-leiautesrn_rtc_ibscbs-v1-03-00-2013-nt007.xlsx`  
**Versão**: v1-03-00-2013-nt007  
**Data de Conversão**: 2026-02-12

---

## 📁 Estrutura de Arquivos

### 🔍 Arquivo de Entrada (Comece Aqui)

**`0_MASTER_INDEX.json`**
- Índice completo de toda a documentação
- Estatísticas gerais
- Referências rápidas
- Guia de uso dos arquivos

### 📖 Documentação Narrativa

**`NFSE_DOCUMENTACAO_COMPLETA.md`**
- Documentação completa em formato Markdown
- Explicações contextuais
- Glossário de termos
- Visão geral de conceitos

**`GUIA_USO_AGENTES_IA.md`**
- Guia específico para agentes de IA
- Exemplos de consultas
- Padrões de uso
- Fluxos de validação

### 📊 Dados Estruturados (JSON)

**`1_servicos_incidencia.json`** (328 registros)
- Lista Nacional de Serviços
- Códigos de tributação
- Regras de incidência do ISSQN
- Informações obrigatórias por serviço

**`2_cenarios_exportacao.json`** (112 registros)
- Cenários de exportação de serviços
- Validações de comércio exterior
- Obrigatoriedade de campos NBS/País/Comex
- Comportamento do sistema

**`3_regras_recepcao_dps.json`** (16 registros)
- Regras de validação na recepção
- Certificados digitais
- Códigos e mensagens de erro
- Aplicação e efeitos

**`4_leiaute_dps_nfse.json`** (431 registros)
- Estrutura completa do XML
- Campos, tipos e tamanhos
- Hierarquia de elementos
- Descrições detalhadas

**`5_regras_validacao_nfse.json`** (677 registros)
- Regras de negócio completas
- Validações por nível (1, 2, 3)
- Códigos de erro
- Contextos de aplicação

---

## 🚀 Quick Start

### Para Agentes de IA

```
1. Leia primeiro: 0_MASTER_INDEX.json
   → Entenda a estrutura geral

2. Consulte: GUIA_USO_AGENTES_IA.md
   → Aprenda como fazer consultas

3. Use os arquivos JSON conforme necessidade:
   → Serviço específico? → 1_servicos_incidencia.json
   → Exportação? → 2_cenarios_exportacao.json
   → Estrutura XML? → 4_leiaute_dps_nfse.json
   → Validação? → 5_regras_validacao_nfse.json
```

### Para Desenvolvedores

```bash
# Carregar dados
import json

# Índice geral
with open('0_MASTER_INDEX.json', 'r', encoding='utf-8') as f:
    index = json.load(f)

# Serviços
with open('1_servicos_incidencia.json', 'r', encoding='utf-8') as f:
    servicos = json.load(f)

# Consultar serviço por código
codigo = 10101
servico = next(s for s in servicos['servicos'] 
               if s['codigo_tributacao'] == codigo)
print(servico)
```

---

## 🎯 Casos de Uso Principais

### 1. Classificar um Serviço

**Pergunta**: "Qual o código de tributação para consultoria em TI?"

**Solução**:
```python
# Buscar em 1_servicos_incidencia.json
servicos = carregar('1_servicos_incidencia.json')
resultado = buscar_por_palavra('consultoria', servicos)
```

**Retorna**: Código, descrição, regras de incidência

---

### 2. Validar Exportação

**Pergunta**: "Como tratar serviço prestado para cliente no exterior?"

**Solução**:
```python
# Buscar em 2_cenarios_exportacao.json
cenarios = carregar('2_cenarios_exportacao.json')
cenario = encontrar_cenario(
    tomador='Exterior',
    local_prestacao='Brasil',
    subitem='10101'
)
```

**Retorna**: Tributação, obrigatoriedade de campos, local de incidência

---

### 3. Estruturar XML

**Pergunta**: "Quais campos são obrigatórios na tag prestador?"

**Solução**:
```python
# Buscar em 4_leiaute_dps_nfse.json
leiaute = carregar('4_leiaute_dps_nfse.json')
campos = filtrar(
    caminho_xml__contains='prestador',
    ocorrencia='1-1'
)
```

**Retorna**: Lista de campos obrigatórios com tipos e tamanhos

---

### 4. Verificar Regras de Validação

**Pergunta**: "Que validações se aplicam ao CPF do prestador?"

**Solução**:
```python
# Buscar em 5_regras_validacao_nfse.json
regras = carregar('5_regras_validacao_nfse.json')
validacoes = filtrar(
    campo__contains='CPF',
    caminho_xml__contains='prestador'
)
```

**Retorna**: Regras, códigos de erro, mensagens, níveis

---

## 📚 Principais Conceitos

### Localidade de Incidência (LI)

Define onde o ISSQN é devido:

- **EP** - Estabelecimento/Domicílio do Prestador
- **LP** - Local da Prestação
- **ET** - Estabelecimento/Domicílio do Tomador
- **EDEmit** - Estabelecimento do Emitente (importação)

### Níveis de Regras

- **Nível 1** - Consistência de leiaute
- **Nível 2** - Regras nacionais (todos os municípios)
- **Nível 3** - Regras municipais específicas

### Ocorrências de Campos

- **1-1** - Obrigatório (exatamente 1 vez)
- **0-1** - Opcional (0 ou 1 vez)
- **1-N** - Obrigatório (1 ou mais vezes)
- **0-N** - Opcional (0 ou mais vezes)

---

## 🔍 Exemplos de Consultas

### Buscar Serviço por Código
```python
codigo = 10101
servico = next(
    s for s in servicos['servicos']
    if s['codigo_tributacao'] == codigo
)
```

### Listar Serviços com Incidência no Local de Prestação
```python
servicos_lp = [
    s for s in servicos['servicos']
    if s['localidade_incidencia']['local_prestacao'] == 'X'
]
```

### Encontrar Campos Obrigatórios de um Grupo
```python
campos_obrig = [
    c for c in leiaute['campos']
    if 'prestador' in c['caminho_xml'].lower()
    and '1-1' in c['ocorrencia']
]
```

### Filtrar Regras de Nível Municipal
```python
regras_munic = [
    r for r in regras['regras']
    if r['nivel_regra'] == '3'
]
```

---

## ⚠️ Casos Especiais

### Águas Marítimas
- **Código**: 0000000
- **Regra**: Permitido para todos os serviços EXCETO 200101
- **Incidência**: EDP (Estabelecimento do Prestador)

### Importação de Serviços
- **Identificação**: Emitente = T ou I + País Exterior
- **Incidência**: EDEmit (prevalece sobre LC 116/03)

### Decisão Judicial
- **Status**: cStat = 102
- **Efeito**: Algumas validações não são executadas

---

## 📊 Estatísticas da Documentação

- **328 serviços** na Lista Nacional
- **112 cenários** de exportação
- **16 regras** de recepção DPS
- **431 campos** no leiaute XML
- **677 regras** de validação

**Total**: Mais de 1.500 pontos de dados estruturados

---

## 🛠️ Tecnologias e Formatos

- **JSON**: UTF-8, estruturado, validado
- **Markdown**: CommonMark, navegável, legível
- **Compatibilidade**: Python 3.x, JavaScript, qualquer linguagem com parser JSON

---

## 📖 Glossário Rápido

| Termo | Significado |
|-------|-------------|
| ADN | Ambiente de Dados Nacionais |
| DPS | Declaração de Prestação de Serviço |
| EP | Estabelecimento do Prestador |
| ET | Estabelecimento do Tomador |
| ISSQN | Imposto Sobre Serviços de Qualquer Natureza |
| LC 116/03 | Lei Complementar 116 de 2003 |
| LI | Localidade de Incidência |
| LP | Local de Prestação |
| NBS | Nomenclatura Brasileira de Serviços |
| NFS-e | Nota Fiscal de Serviço Eletrônica |
| RFB | Receita Federal do Brasil |

---

## 📝 Notas Importantes

1. **Encoding**: Todos os arquivos JSON usam UTF-8
2. **Null Values**: Campos não aplicáveis podem conter `null`
3. **Arrays**: Sempre encapsulados em objeto pai com metadados
4. **Versionamento**: Documentação baseada em v1-03-00-2013-nt007

---

## 🔄 Atualizações

Esta documentação é uma conversão fiel do arquivo Excel original.

Para versões mais recentes:
- Consulte o site oficial do Sistema Nacional NFS-e
- Verifique notas técnicas posteriores
- Compare versões de leiaute

---

## 💡 Dicas de Uso

### Para Máxima Eficiência

1. **Carregue uma vez**: Mantenha os JSONs em memória
2. **Index estratégico**: Crie índices por código, descrição, caminho XML
3. **Cache resultados**: Consultas repetidas devem usar cache
4. **Validação progressiva**: Estrutura → Certificados → Negócio
5. **Contexto completo**: Sempre considere tipo de serviço + localidades

### Para Melhor Precisão

1. **Combine fontes**: Use múltiplos arquivos para contexto completo
2. **Siga hierarquia**: Nível 3 > Nível 2 > Nível 1
3. **Considere exceções**: Importação, exportação, águas marítimas
4. **Valide códigos**: CPF/CNPJ, códigos de serviço, municípios
5. **Use códigos de erro oficiais**: Sempre referencie o EXXXX

---

## 📧 Suporte

Para dúvidas sobre a documentação técnica original:
- Consulte o Sistema Nacional NFS-e oficial
- Verifique a Lei Complementar 116/2003
- Revise portarias e instruções normativas aplicáveis

Para dúvidas sobre esta conversão:
- Todos os dados foram extraídos automaticamente
- Estrutura 100% preservada do original
- Formato otimizado para processamento automatizado

---

**Versão do README**: 1.0  
**Última Atualização**: 2026-02-12  
**Compatibilidade**: Agentes de IA, Python 3.x, JavaScript ES6+, qualquer sistema com parser JSON
