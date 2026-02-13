# Guia Completo de Automação - Conversão de Leiaute NFS-e

## 🎯 Objetivo

Este guia garante que toda nova versão do leiaute NFS-e seja convertida seguindo **EXATAMENTE** o mesmo padrão, mantendo compatibilidade total com seu portal web SPA.

---

## 📦 Pacote de Automação

Você tem 3 opções para converter novas versões:

### Opção 1: Script Python Automatizado (Recomendado)
✅ Mais rápido  
✅ Mais confiável  
✅ Sem dependência de IA  

### Opção 2: Prompt para IA
✅ Flexível  
✅ Funciona com qualquer IA  
✅ Não requer Python  

### Opção 3: Híbrida
✅ Script Python + validação por IA  
✅ Melhor dos dois mundos  

---

## 🚀 Opção 1: Script Python Automatizado

### Pré-requisitos

```bash
# Instalar dependências
pip install openpyxl
```

### Uso

```bash
# Converter arquivo
python converter_nfse.py leiaute-nova-versao.xlsx

# Validar saída
python validar_nfse.py output_nfse/
```

### Workflow Completo

```bash
#!/bin/bash
# Script: processar_nova_versao.sh

ARQUIVO_EXCEL="$1"

if [ -z "$ARQUIVO_EXCEL" ]; then
    echo "Uso: ./processar_nova_versao.sh <arquivo.xlsx>"
    exit 1
fi

echo "🚀 Processando nova versão do leiaute NFS-e"
echo "📄 Arquivo: $ARQUIVO_EXCEL"

# 1. Converter
echo "⚙️  Executando conversão..."
python3 converter_nfse.py "$ARQUIVO_EXCEL"

if [ $? -ne 0 ]; then
    echo "❌ Erro na conversão"
    exit 1
fi

# 2. Validar
echo "🔍 Validando arquivos gerados..."
python3 validar_nfse.py output_nfse/

if [ $? -ne 0 ]; then
    echo "⚠️  Arquivos gerados, mas há avisos de validação"
    exit 1
fi

# 3. Sucesso
echo "✅ Conversão concluída e validada!"
echo "📁 Arquivos disponíveis em: output_nfse/"

# 4. Opcional: copiar para diretório do portal
# cp output_nfse/*.json ../meu-portal/src/data/
# cp output_nfse/*.md ../meu-portal/public/docs/

exit 0
```

---

## 🤖 Opção 2: Prompt para IA

### Como Usar

1. **Copie o conteúdo de `PROMPT_REUTILIZAVEL.md`**

2. **Cole na conversa com a IA** (Claude, ChatGPT, etc.)

3. **Faça upload do arquivo Excel**

4. **Aguarde a conversão**

5. **Baixe os arquivos gerados**

6. **Valide com o script**:
   ```bash
   python validar_nfse.py diretorio_baixado/
   ```

### Vantagens

- ✅ Funciona sem instalar Python
- ✅ Pode usar qualquer IA
- ✅ Flexível para ajustes

### Desvantagens

- ⚠️ Depende da IA estar disponível
- ⚠️ Pode ter pequenas variações
- ⚠️ Requer validação manual

---

## 🔄 Opção 3: Híbrida (Melhor Abordagem)

### Workflow

```
1. Script Python converte → output_nfse/
2. IA revisa e gera documentação adicional
3. Script valida tudo
4. Deploy para o portal
```

### Exemplo

```bash
# 1. Conversão automática
python converter_nfse.py nova_versao.xlsx

# 2. Enviar para IA revisar documentação
# (manualmente ou via API)

# 3. Validação final
python validar_nfse.py output_nfse/

# 4. Deploy
./deploy_to_portal.sh
```

---

## 📋 Checklist de Conversão

Use este checklist sempre que converter uma nova versão:

### Antes da Conversão

- [ ] Baixar novo arquivo Excel oficial
- [ ] Verificar nome do arquivo (para extração de versão)
- [ ] Fazer backup da versão anterior
- [ ] Limpar diretório de saída

### Durante a Conversão

- [ ] Executar script ou prompt
- [ ] Monitorar saída em busca de erros
- [ ] Verificar todos os 10 arquivos gerados

### Após a Conversão

- [ ] Executar validador
- [ ] Verificar totais de registros
- [ ] Comparar com versão anterior (diferenças esperadas)
- [ ] Testar no portal (ambiente de dev)
- [ ] Revisar documentação Markdown

### Antes do Deploy

- [ ] Todos os testes passaram
- [ ] Documentação revisada
- [ ] Versão atualizada em todos os arquivos
- [ ] Commit no Git com tag de versão

---

## 🔍 Validação de Consistência

### Validações Automáticas

O script `validar_nfse.py` verifica:

1. **Arquivos obrigatórios**: Todos os 10 arquivos presentes
2. **Estrutura JSON**: Sintaxe válida
3. **Campos obrigatórios**: Presença de campos-chave
4. **Consistência de totais**: Totais batem com arrays
5. **Encoding**: UTF-8 em todos os arquivos

### Validações Manuais Recomendadas

```python
# validacao_manual.py

import json

def validar_versao_consistente():
    """Verifica se versão é consistente em todos os arquivos"""
    arquivos = [
        '0_MASTER_INDEX.json',
        '1_servicos_incidencia.json',
        '2_cenarios_exportacao.json',
        '3_regras_recepcao_dps.json',
        '4_leiaute_dps_nfse.json',
        '5_regras_validacao_nfse.json'
    ]
    
    versoes = set()
    
    for arquivo in arquivos:
        with open(f'output_nfse/{arquivo}', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'versao' in data:
                versoes.add(data['versao'])
    
    if len(versoes) > 1:
        print(f"⚠️  AVISO: Versões inconsistentes: {versoes}")
        return False
    
    print(f"✅ Versão consistente: {list(versoes)[0]}")
    return True

def comparar_com_versao_anterior(dir_atual, dir_anterior):
    """Compara estrutura com versão anterior"""
    # Implementar comparação de schemas
    pass

if __name__ == "__main__":
    validar_versao_consistente()
```

---

## 🛠️ Troubleshooting

### Problema: Aba não encontrada

**Sintoma**: "⚠️ Aba de serviços não encontrada"

**Solução**: O Excel pode ter nome de aba diferente. Atualize o script:

```python
# No converter_nfse.py, adicione novo nome possível
sheet_names = ['MUN.INCID_INFO.SERV.', 'SERVICOS', 'LISTA_SERVICOS', 'NOVO_NOME']
```

### Problema: Estrutura de colunas mudou

**Sintoma**: Campos com valores errados

**Solução**: Verifique índices das colunas no Excel e ajuste:

```python
# Exemplo: Se código mudou da coluna 0 para 1
servico = {
    "codigo_tributacao": int(row[1]),  # Era row[0]
    "descricao": row[2],                # Era row[1]
    # ...
}
```

### Problema: Validação falha

**Sintoma**: Script validador retorna erros

**Solução**: 

1. Verifique mensagem de erro específica
2. Corrija manualmente o JSON se necessário
3. Execute validador novamente
4. Se problema persistir, use prompt de IA para regenerar

### Problema: Versão não detectada

**Sintoma**: `versao: "versao-desconhecida"`

**Solução**: Ajuste regex de extração:

```python
def _extract_version(self, filename):
    # Tente padrões diferentes
    patterns = [
        r'v\d+-\d+-\d+-\d+-nt\d+',  # Padrão atual
        r'v\d+\.\d+\.\d+',           # Alternativo
        r'versao-\d+-\d+'            # Outro alternativo
    ]
    # Implementar tentativa com múltiplos padrões
```

---

## 📊 Comparação de Versões

### Script para Comparar Versões

```python
# comparar_versoes.py

import json
from pathlib import Path

def comparar_servicos(v1_path, v2_path):
    """Compara lista de serviços entre versões"""
    
    with open(v1_path, 'r', encoding='utf-8') as f:
        v1 = json.load(f)
    
    with open(v2_path, 'r', encoding='utf-8') as f:
        v2 = json.load(f)
    
    codigos_v1 = {s['codigo_tributacao'] for s in v1['servicos']}
    codigos_v2 = {s['codigo_tributacao'] for s in v2['servicos']}
    
    novos = codigos_v2 - codigos_v1
    removidos = codigos_v1 - codigos_v2
    
    print(f"\n📊 Comparação de Serviços")
    print(f"  Versão 1: {len(codigos_v1)} serviços")
    print(f"  Versão 2: {len(codigos_v2)} serviços")
    
    if novos:
        print(f"\n  ✨ Novos ({len(novos)}): {sorted(novos)}")
    
    if removidos:
        print(f"\n  🗑️  Removidos ({len(removidos)}): {sorted(removidos)}")
    
    if not novos and not removidos:
        print(f"\n  ✅ Mesmos códigos de serviço")

if __name__ == "__main__":
    comparar_servicos(
        'versao_anterior/1_servicos_incidencia.json',
        'output_nfse/1_servicos_incidencia.json'
    )
```

---

## 🌐 Integração com o Portal

### Estrutura Sugerida no Portal

```
meu-portal/
├── src/
│   └── data/
│       ├── nfse/
│       │   ├── v1-03-00-2013-nt007/
│       │   │   ├── 1_servicos_incidencia.json
│       │   │   ├── 2_cenarios_exportacao.json
│       │   │   └── ...
│       │   └── v2-00-00-2024-nt008/  ← Nova versão
│       │       ├── 1_servicos_incidencia.json
│       │       └── ...
│       └── current_version.json
└── public/
    └── docs/
        └── nfse/
            ├── v1-03-00-2013-nt007/
            │   └── *.md
            └── v2-00-00-2024-nt008/
                └── *.md
```

### Script de Deploy

```bash
#!/bin/bash
# deploy_to_portal.sh

VERSAO=$(python3 -c "import json; print(json.load(open('output_nfse/0_MASTER_INDEX.json'))['versao'])")
PORTAL_DIR="../meu-portal"

echo "📦 Fazendo deploy da versão: $VERSAO"

# Criar diretórios
mkdir -p "$PORTAL_DIR/src/data/nfse/$VERSAO"
mkdir -p "$PORTAL_DIR/public/docs/nfse/$VERSAO"

# Copiar JSONs
cp output_nfse/*.json "$PORTAL_DIR/src/data/nfse/$VERSAO/"

# Copiar Markdowns
cp output_nfse/*.md "$PORTAL_DIR/public/docs/nfse/$VERSAO/"

# Atualizar versão atual
echo "{\"current_version\": \"$VERSAO\"}" > "$PORTAL_DIR/src/data/current_version.json"

echo "✅ Deploy concluído!"
echo "📁 Arquivos em: $PORTAL_DIR/src/data/nfse/$VERSAO/"
```

---

## 🔐 Controle de Qualidade

### Testes Automatizados

```python
# test_conversao.py

import unittest
import json
from pathlib import Path

class TestConversaoNFSe(unittest.TestCase):
    
    def setUp(self):
        self.output_dir = Path('output_nfse')
        
    def test_todos_arquivos_presentes(self):
        """Verifica se todos os 10 arquivos foram gerados"""
        arquivos_esperados = [
            '0_MASTER_INDEX.json',
            '1_servicos_incidencia.json',
            '2_cenarios_exportacao.json',
            '3_regras_recepcao_dps.json',
            '4_leiaute_dps_nfse.json',
            '5_regras_validacao_nfse.json',
            'README.md',
            'NFSE_DOCUMENTACAO_COMPLETA.md',
            'GUIA_USO_AGENTES_IA.md',
            'SUMARIO_CONVERSAO.md'
        ]
        
        for arquivo in arquivos_esperados:
            self.assertTrue(
                (self.output_dir / arquivo).exists(),
                f"Arquivo {arquivo} não encontrado"
            )
    
    def test_json_valido(self):
        """Verifica se todos os JSONs são válidos"""
        json_files = self.output_dir.glob('*.json')
        
        for filepath in json_files:
            with self.subTest(arquivo=filepath.name):
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        json.load(f)
                    except json.JSONDecodeError as e:
                        self.fail(f"JSON inválido em {filepath.name}: {e}")
    
    def test_campos_obrigatorios_master(self):
        """Verifica campos obrigatórios no MASTER_INDEX"""
        with open(self.output_dir / '0_MASTER_INDEX.json', 'r') as f:
            data = json.load(f)
        
        self.assertIn('documento', data)
        self.assertIn('versao', data)
        self.assertIn('estatisticas', data)
    
    def test_totais_consistentes(self):
        """Verifica se totais são consistentes"""
        with open(self.output_dir / '0_MASTER_INDEX.json', 'r') as f:
            master = json.load(f)
        
        with open(self.output_dir / '1_servicos_incidencia.json', 'r') as f:
            servicos = json.load(f)
        
        self.assertEqual(
            len(servicos['servicos']),
            master['estatisticas']['total_servicos']
        )

if __name__ == '__main__':
    unittest.main()
```

### Executar Testes

```bash
# Executar testes
python -m unittest test_conversao.py

# Com cobertura
pip install coverage
coverage run -m unittest test_conversao.py
coverage report
```

---

## 📝 Documentação de Mudanças

### Template de CHANGELOG

```markdown
# CHANGELOG - Leiaute NFS-e

## [v2-00-00-2024-nt008] - 2024-03-15

### Adicionado
- 15 novos serviços na lista nacional
- 8 novos cenários de exportação
- Validação para campo XYZ

### Modificado
- Descrição do serviço 10101 atualizada
- Regra de incidência para serviço 20301 alterada

### Removido
- Nenhum serviço removido

### Estatísticas
- Serviços: 328 → 343 (+15)
- Cenários: 112 → 120 (+8)
- Regras: 677 → 685 (+8)

## [v1-03-00-2013-nt007] - 2013-00-03

### Versão Inicial
- 328 serviços
- 112 cenários
- 677 regras
```

---

## 🎓 Melhores Práticas

### 1. Versionamento

- Use Git para versionar os arquivos gerados
- Crie tags para cada versão do leiaute
- Mantenha histórico de conversões

```bash
git tag -a v2-00-00-2024-nt008 -m "Leiaute NFS-e v2"
git push origin v2-00-00-2024-nt008
```

### 2. Automação CI/CD

Integre com GitHub Actions ou similar:

```yaml
# .github/workflows/converter-nfse.yml

name: Converter Leiaute NFS-e

on:
  push:
    paths:
      - 'leiaute/*.xlsx'

jobs:
  convert:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install openpyxl
      
      - name: Convert
        run: python converter_nfse.py leiaute/*.xlsx
      
      - name: Validate
        run: python validar_nfse.py output_nfse/
      
      - name: Deploy
        run: ./deploy_to_portal.sh
```

### 3. Backup

Sempre faça backup antes de converter:

```bash
# backup.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "backup_nfse_$TIMESTAMP.tar.gz" output_nfse/
```

---

## 📞 Suporte

### Problemas Comuns

1. **Script não executa**: Verificar Python 3.7+
2. **JSON inválido**: Executar validador
3. **Totais inconsistentes**: Revisar extração do Excel
4. **Versão errada**: Ajustar regex de extração

### Contatos

- Documentação: Este guia
- Issues: GitHub do projeto
- Validador: `python validar_nfse.py --help`

---

## ✅ Resumo Executivo

Para converter nova versão do leiaute:

```bash
# Opção rápida (recomendada)
python converter_nfse.py nova_versao.xlsx && \
python validar_nfse.py output_nfse/ && \
./deploy_to_portal.sh

# Ou use o prompt de IA e depois valide
python validar_nfse.py diretorio_ia/
```

**Tempo estimado**: 2-5 minutos  
**Arquivos gerados**: 10  
**Compatibilidade**: 100% com padrão estabelecido
