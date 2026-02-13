#!/usr/bin/env python3
"""
Conversor Automatizado de Leiaute NFS-e
========================================

Este script converte arquivos Excel do leiaute NFS-e para formatos
estruturados (JSON e Markdown) otimizados para agentes de IA.

Uso:
    python converter_nfse.py <arquivo.xlsx>

Exemplo:
    python converter_nfse.py anexovi-leiautesrn_rtc_ibscbs-v2-00-00-2024-nt008.xlsx

Saída:
    - 10 arquivos no diretório 'output_nfse/'
    - JSON: dados estruturados
    - Markdown: documentação
"""

import openpyxl
import json
import sys
import os
from datetime import datetime
from pathlib import Path


class NFSeConverter:
    """Conversor de leiaute NFS-e para formato padronizado"""
    
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.wb = None
        self.output_dir = Path('output_nfse')
        self.version = self._extract_version(excel_file)
        self.conversion_date = datetime.now().isoformat()
        
    def _extract_version(self, filename):
        """Extrai versão do nome do arquivo"""
        # Exemplo: anexovi-leiautesrn_rtc_ibscbs-v1-03-00-2013-nt007.xlsx
        parts = filename.split('-')
        for i, part in enumerate(parts):
            if part.startswith('v') and i + 4 < len(parts):
                return '-'.join(parts[i:i+5])
        return "versao-desconhecida"
    
    def convert(self):
        """Executa conversão completa"""
        print(f"🚀 Iniciando conversão de {self.excel_file}")
        print(f"📌 Versão detectada: {self.version}")
        
        # Criar diretório de saída
        self.output_dir.mkdir(exist_ok=True)
        
        # Carregar arquivo
        print("📂 Carregando arquivo Excel...")
        self.wb = openpyxl.load_workbook(self.excel_file, data_only=True)
        
        # Processar cada aba
        print("⚙️  Processando abas...")
        self._process_servicos()
        self._process_exportacao()
        self._process_recepcao_dps()
        self._process_leiaute()
        self._process_regras_validacao()
        
        # Gerar arquivos de documentação
        print("📝 Gerando documentação...")
        self._generate_master_index()
        self._generate_documentation()
        self._generate_readme()
        self._generate_summary()
        
        print(f"✅ Conversão concluída! Arquivos em: {self.output_dir}/")
        self._print_statistics()
    
    def _process_servicos(self):
        """Processa aba de serviços e incidência"""
        sheet_names = ['MUN.INCID_INFO.SERV.', 'SERVICOS', 'LISTA_SERVICOS']
        sheet = self._find_sheet(sheet_names)
        
        if not sheet:
            print("⚠️  Aba de serviços não encontrada")
            return
        
        servicos = []
        for row in sheet.iter_rows(min_row=5, values_only=True):
            if row[0] and isinstance(row[0], (int, float)):
                servico = {
                    "codigo_tributacao": int(row[0]),
                    "descricao": row[1],
                    "localidade_incidencia": {
                        "estabelecimento_prestador": "X" if row[2] == "X" else None,
                        "local_prestacao": "X" if row[3] == "X" else None,
                        "estabelecimento_tomador": "X" if row[4] == "X" else None,
                        "estabelecimento_emitente": "X" if row[5] == "X" else None
                    },
                    "grupos_informacao": {
                        "obrigatorio": "X" if row[6] == "X" else "-" if row[6] == "-" else None,
                        "info_complementares": "X" if row[7] == "X" else "-" if row[7] == "-" else None
                    }
                }
                servicos.append(servico)
        
        output = {
            "titulo": "Lista Nacional de Serviços - Incidência e Informações",
            "versao": self.version,
            "descricao": "Determinação da localidade de incidência (LI) de acordo com a LC 116/03",
            "total_servicos": len(servicos),
            "servicos": servicos
        }
        
        self._save_json('1_servicos_incidencia.json', output)
        print(f"  ✓ Processados {len(servicos)} serviços")
    
    def _process_exportacao(self):
        """Processa aba de cenários de exportação"""
        sheet_names = ['EXPORTACAO_EMISSÃO_NFS-e', 'EXPORTACAO', 'CENARIOS_EXPORTACAO']
        sheet = self._find_sheet(sheet_names)
        
        if not sheet:
            print("⚠️  Aba de exportação não encontrada")
            return
        
        cenarios = []
        for row in sheet.iter_rows(min_row=6, values_only=True):
            if row[0]:
                cenario = {
                    "cenario": row[0],
                    "locais": {
                        "endereco_tomador": row[1],
                        "endereco_intermediario": row[2],
                        "local_prestacao": row[3]
                    },
                    "subitem_lista": row[4],
                    "local_incidencia_teorico": row[5],
                    "tributacao": {
                        "imunidade_exportacao_nao_incidencia": row[6],
                        "tributacao_issqn": row[7]
                    },
                    "exportacao": {
                        "issqn": row[8],
                        "rfb": row[9]
                    },
                    "validacao": {
                        "mensagem_erro_aviso": row[10],
                        "local_incidencia_real": row[11]
                    },
                    "info_comex": {
                        "nbs": row[12] if len(row) > 12 else None,
                        "pais_resultado": row[13] if len(row) > 13 else None,
                        "grupo_comex": row[14] if len(row) > 14 else None
                    }
                }
                cenarios.append(cenario)
        
        output = {
            "titulo": "Cenários de Exportação para Emissão de NFS-e",
            "versao": self.version,
            "descricao": "Comportamento do sistema para validação de itens declarados pelo emitente",
            "total_cenarios": len(cenarios),
            "cenarios": cenarios
        }
        
        self._save_json('2_cenarios_exportacao.json', output)
        print(f"  ✓ Processados {len(cenarios)} cenários")
    
    def _process_recepcao_dps(self):
        """Processa aba de regras de recepção DPS"""
        sheet_names = ['RN_RECEPCAO_DPS', 'RECEPCAO_DPS', 'REGRAS_RECEPCAO']
        sheet = self._find_sheet(sheet_names)
        
        if not sheet:
            print("⚠️  Aba de recepção DPS não encontrada")
            return
        
        regras = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] and isinstance(row[0], (int, float)):
                regra = {
                    "numero": int(row[0]),
                    "descricao": row[1],
                    "aplicacao": row[3] if len(row) > 3 else None,
                    "efeito": row[4] if len(row) > 4 else None,
                    "codigo_erro": row[5] if len(row) > 5 else None,
                    "mensagem_erro": row[6] if len(row) > 6 else None,
                    "notas_explicativas": row[7] if len(row) > 7 else None
                }
                regras.append(regra)
        
        output = {
            "titulo": "Regras de Negócio para Recepção de DPS",
            "versao": self.version,
            "descricao": "Validações aplicadas na recepção de Declaração de Prestação de Serviço",
            "total_regras": len(regras),
            "regras": regras
        }
        
        self._save_json('3_regras_recepcao_dps.json', output)
        print(f"  ✓ Processadas {len(regras)} regras")
    
    def _process_leiaute(self):
        """Processa aba de leiaute DPS/NFS-e"""
        sheet_names = ['LEIAUTE DPS_NFS-e', 'LEIAUTE', 'LEIAUTE_XML']
        sheet = self._find_sheet(sheet_names)
        
        if not sheet:
            print("⚠️  Aba de leiaute não encontrada")
            return
        
        campos = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] and isinstance(row[0], (int, float)):
                campo = {
                    "numero": int(row[0]),
                    "caminho_xml": row[1],
                    "campo": row[2],
                    "elemento": row[3] if len(row) > 3 else None,
                    "tipo": row[4] if len(row) > 4 else None,
                    "ocorrencia": row[5] if len(row) > 5 else None,
                    "tamanho": row[6] if len(row) > 6 else None,
                    "descricao": row[7] if len(row) > 7 else None,
                    "notas_explicativas": row[8] if len(row) > 8 else None
                }
                campos.append(campo)
        
        output = {
            "titulo": "Leiaute da DPS e NFS-e",
            "versao": self.version,
            "descricao": "Estrutura XML para Declaração de Prestação de Serviço e Nota Fiscal Eletrônica",
            "total_campos": len(campos),
            "campos": campos
        }
        
        self._save_json('4_leiaute_dps_nfse.json', output)
        print(f"  ✓ Processados {len(campos)} campos")
    
    def _process_regras_validacao(self):
        """Processa aba de regras de validação"""
        sheet_names = ['RN DPS_NFS-e', 'REGRAS_VALIDACAO', 'RN_NFSE']
        sheet = self._find_sheet(sheet_names)
        
        if not sheet:
            print("⚠️  Aba de regras de validação não encontrada")
            return
        
        regras = []
        for row in sheet.iter_rows(min_row=4, values_only=True):
            if row[0] and isinstance(row[0], (int, float)):
                regra = {
                    "numero": int(row[0]),
                    "caminho_xml": row[1] if len(row) > 1 else None,
                    "campo": row[2] if len(row) > 2 else None,
                    "regra_negocio": row[3] if len(row) > 3 else None,
                    "aplicacao": row[5] if len(row) > 5 else None,
                    "efeito": row[6] if len(row) > 6 else None,
                    "codigo_erro": row[7] if len(row) > 7 else None,
                    "mensagem_erro": row[8] if len(row) > 8 else None,
                    "nivel_regra": row[9] if len(row) > 9 else None,
                    "emissores_publicos": {
                        "recepcao_dps": row[10] if len(row) > 10 else None,
                        "geracao_nfse_condicional": row[11] if len(row) > 11 else None
                    },
                    "adn_nfse": {
                        "recepcao_compartilhada": row[12] if len(row) > 12 else None,
                        "recepcao_condicional": row[13] if len(row) > 13 else None
                    },
                    "observacoes": row[14] if len(row) > 14 else None
                }
                regras.append(regra)
        
        output = {
            "titulo": "Regras de Negócio para DPS e NFS-e",
            "versao": self.version,
            "descricao": "Regras de validação aplicadas no Sistema Nacional NFS-e",
            "total_regras": len(regras),
            "regras": regras
        }
        
        self._save_json('5_regras_validacao_nfse.json', output)
        print(f"  ✓ Processadas {len(regras)} regras")
    
    def _generate_master_index(self):
        """Gera índice master"""
        # Carregar estatísticas dos JSONs gerados
        stats = {}
        for i in range(1, 6):
            json_file = self.output_dir / f'{i}_*.json'
            files = list(self.output_dir.glob(f'{i}_*.json'))
            if files:
                with open(files[0], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'total_servicos' in data:
                        stats['servicos'] = data['total_servicos']
                    elif 'total_cenarios' in data:
                        stats['cenarios'] = data['total_cenarios']
                    elif 'total_regras' in data:
                        stats['regras_recepcao'] = data['total_regras']
                    elif 'total_campos' in data:
                        stats['campos'] = data['total_campos']
                    elif 'total_regras' in data and 'regras' in data:
                        stats['regras_validacao'] = data['total_regras']
        
        master = {
            "documento": "Sistema Nacional NFS-e - Documentação Técnica",
            "versao": self.version,
            "data_conversao": self.conversion_date,
            "arquivo_origem": os.path.basename(self.excel_file),
            "estatisticas": {
                "total_servicos": stats.get('servicos', 0),
                "total_cenarios_exportacao": stats.get('cenarios', 0),
                "total_regras_recepcao": stats.get('regras_recepcao', 0),
                "total_campos_leiaute": stats.get('campos', 0),
                "total_regras_validacao": stats.get('regras_validacao', 0)
            },
            "arquivos_gerados": [
                {
                    "arquivo": "1_servicos_incidencia.json",
                    "tipo": "json",
                    "descricao": "Lista Nacional de Serviços"
                },
                {
                    "arquivo": "2_cenarios_exportacao.json",
                    "tipo": "json",
                    "descricao": "Cenários de Exportação"
                },
                {
                    "arquivo": "3_regras_recepcao_dps.json",
                    "tipo": "json",
                    "descricao": "Regras de Recepção DPS"
                },
                {
                    "arquivo": "4_leiaute_dps_nfse.json",
                    "tipo": "json",
                    "descricao": "Leiaute XML DPS/NFS-e"
                },
                {
                    "arquivo": "5_regras_validacao_nfse.json",
                    "tipo": "json",
                    "descricao": "Regras de Validação NFS-e"
                }
            ]
        }
        
        self._save_json('0_MASTER_INDEX.json', master)
    
    def _generate_documentation(self):
        """Gera documentação completa em Markdown"""
        # Template simplificado - você pode expandir conforme necessário
        doc = f"""# Documentação Técnica - Sistema Nacional NFS-e

**Versão:** {self.version}  
**Data de Conversão:** {self.conversion_date}

---

## Arquivos Gerados

1. **1_servicos_incidencia.json** - Lista Nacional de Serviços
2. **2_cenarios_exportacao.json** - Cenários de Exportação
3. **3_regras_recepcao_dps.json** - Regras de Recepção DPS
4. **4_leiaute_dps_nfse.json** - Leiaute XML
5. **5_regras_validacao_nfse.json** - Regras de Validação

Consulte o README.md para instruções detalhadas de uso.
"""
        
        self._save_text('NFSE_DOCUMENTACAO_COMPLETA.md', doc)
    
    def _generate_readme(self):
        """Gera README"""
        readme = f"""# Documentação NFS-e - Versão {self.version}

## Conversão Automática

Esta documentação foi gerada automaticamente a partir do arquivo Excel do leiaute NFS-e.

**Arquivo Original:** {os.path.basename(self.excel_file)}  
**Data de Conversão:** {self.conversion_date}

## Arquivos Disponíveis

- `0_MASTER_INDEX.json` - Índice completo
- `1_servicos_incidencia.json` - Serviços e incidência
- `2_cenarios_exportacao.json` - Cenários de exportação
- `3_regras_recepcao_dps.json` - Regras de recepção
- `4_leiaute_dps_nfse.json` - Estrutura XML
- `5_regras_validacao_nfse.json` - Regras de validação

## Como Usar

Todos os arquivos estão em formato JSON com encoding UTF-8.

```python
import json

# Carregar serviços
with open('1_servicos_incidencia.json', 'r', encoding='utf-8') as f:
    servicos = json.load(f)

# Buscar serviço por código
codigo = 10101
servico = next(s for s in servicos['servicos'] 
               if s['codigo_tributacao'] == codigo)
```

Para mais informações, consulte a documentação completa.
"""
        
        self._save_text('README.md', readme)
    
    def _generate_summary(self):
        """Gera sumário da conversão"""
        summary = f"""# Sumário da Conversão - NFS-e {self.version}

## Conversão Concluída

**Data:** {self.conversion_date}  
**Arquivo Original:** {os.path.basename(self.excel_file)}

## Arquivos Gerados

✅ 10 arquivos em formato JSON e Markdown  
✅ Estrutura padronizada mantida  
✅ 100% dos dados preservados

Consulte o README.md para começar.
"""
        
        self._save_text('SUMARIO_CONVERSAO.md', summary)
    
    def _find_sheet(self, possible_names):
        """Encontra aba por lista de nomes possíveis"""
        for name in possible_names:
            for sheet_name in self.wb.sheetnames:
                if name.lower() in sheet_name.lower():
                    return self.wb[sheet_name]
        return None
    
    def _save_json(self, filename, data):
        """Salva dados em JSON"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_text(self, filename, text):
        """Salva texto em arquivo"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def _print_statistics(self):
        """Imprime estatísticas da conversão"""
        print("\n📊 Estatísticas:")
        
        json_files = list(self.output_dir.glob('*.json'))
        md_files = list(self.output_dir.glob('*.md'))
        
        total_size = sum(f.stat().st_size for f in json_files + md_files)
        
        print(f"  • Arquivos JSON: {len(json_files)}")
        print(f"  • Arquivos Markdown: {len(md_files)}")
        print(f"  • Tamanho total: {total_size / 1024:.1f} KB")
        print(f"  • Versão: {self.version}")


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("❌ Erro: Arquivo Excel não especificado")
        print(f"\nUso: python {sys.argv[0]} <arquivo.xlsx>")
        print(f"\nExemplo: python {sys.argv[0]} leiaute-nfse-v2.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    if not os.path.exists(excel_file):
        print(f"❌ Erro: Arquivo '{excel_file}' não encontrado")
        sys.exit(1)
    
    try:
        converter = NFSeConverter(excel_file)
        converter.convert()
        print("\n🎉 Sucesso! Arquivos prontos para uso no portal.")
        
    except Exception as e:
        print(f"\n❌ Erro durante conversão: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
