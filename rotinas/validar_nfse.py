#!/usr/bin/env python3
"""
Validador de Arquivos NFS-e
============================

Valida se os arquivos JSON gerados seguem o padrão estabelecido.

Uso:
    python validar_nfse.py <diretorio>

Exemplo:
    python validar_nfse.py output_nfse/
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple


class NFSeValidator:
    """Valida arquivos NFS-e contra o padrão estabelecido"""
    
    REQUIRED_FILES = [
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
    
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.errors = []
        self.warnings = []
        
    def validate(self) -> bool:
        """Executa todas as validações"""
        print(f"🔍 Validando arquivos em: {self.directory}")
        
        # Validação 1: Arquivos obrigatórios
        self._validate_required_files()
        
        # Validação 2: Estrutura JSON
        self._validate_json_structure()
        
        # Validação 3: Consistência de dados
        self._validate_data_consistency()
        
        # Validação 4: Encoding
        self._validate_encoding()
        
        # Resultados
        self._print_results()
        
        return len(self.errors) == 0
    
    def _validate_required_files(self):
        """Valida presença de arquivos obrigatórios"""
        print("\n📁 Validando arquivos obrigatórios...")
        
        for filename in self.REQUIRED_FILES:
            filepath = self.directory / filename
            if not filepath.exists():
                self.errors.append(f"Arquivo obrigatório ausente: {filename}")
            else:
                print(f"  ✓ {filename}")
    
    def _validate_json_structure(self):
        """Valida estrutura dos arquivos JSON"""
        print("\n📊 Validando estrutura JSON...")
        
        json_files = [f for f in self.REQUIRED_FILES if f.endswith('.json')]
        
        for filename in json_files:
            filepath = self.directory / filename
            if not filepath.exists():
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validações específicas por arquivo
                if filename == '0_MASTER_INDEX.json':
                    self._validate_master_index(data)
                elif filename.startswith('1_'):
                    self._validate_servicos(data)
                elif filename.startswith('2_'):
                    self._validate_cenarios(data)
                elif filename.startswith('3_'):
                    self._validate_regras_recepcao(data)
                elif filename.startswith('4_'):
                    self._validate_leiaute(data)
                elif filename.startswith('5_'):
                    self._validate_regras_validacao(data)
                
                print(f"  ✓ {filename}: estrutura válida")
                
            except json.JSONDecodeError as e:
                self.errors.append(f"{filename}: JSON inválido - {e}")
            except Exception as e:
                self.errors.append(f"{filename}: erro ao validar - {e}")
    
    def _validate_master_index(self, data: Dict):
        """Valida arquivo 0_MASTER_INDEX.json"""
        required_keys = ['documento', 'versao', 'data_conversao', 'arquivo_origem', 'estatisticas']
        
        for key in required_keys:
            if key not in data:
                self.errors.append(f"0_MASTER_INDEX.json: campo obrigatório '{key}' ausente")
        
        if 'estatisticas' in data:
            stats_keys = ['total_servicos', 'total_cenarios_exportacao', 'total_regras_recepcao', 
                         'total_campos_leiaute', 'total_regras_validacao']
            for key in stats_keys:
                if key not in data['estatisticas']:
                    self.errors.append(f"0_MASTER_INDEX.json: estatística '{key}' ausente")
    
    def _validate_servicos(self, data: Dict):
        """Valida arquivo 1_servicos_incidencia.json"""
        required_keys = ['titulo', 'versao', 'descricao', 'total_servicos', 'servicos']
        
        for key in required_keys:
            if key not in data:
                self.errors.append(f"1_servicos_incidencia.json: campo '{key}' ausente")
        
        # Validar array de serviços
        if 'servicos' in data:
            if not isinstance(data['servicos'], list):
                self.errors.append(f"1_servicos_incidencia.json: 'servicos' deve ser array")
            elif len(data['servicos']) > 0:
                servico = data['servicos'][0]
                required_servico_keys = ['codigo_tributacao', 'descricao', 'localidade_incidencia']
                for key in required_servico_keys:
                    if key not in servico:
                        self.errors.append(f"1_servicos_incidencia.json: serviço sem campo '{key}'")
        
        # Validar total
        if 'servicos' in data and 'total_servicos' in data:
            if len(data['servicos']) != data['total_servicos']:
                self.warnings.append(f"1_servicos_incidencia.json: total_servicos não corresponde ao tamanho do array")
    
    def _validate_cenarios(self, data: Dict):
        """Valida arquivo 2_cenarios_exportacao.json"""
        required_keys = ['titulo', 'versao', 'descricao', 'total_cenarios', 'cenarios']
        
        for key in required_keys:
            if key not in data:
                self.errors.append(f"2_cenarios_exportacao.json: campo '{key}' ausente")
        
        # Validar total
        if 'cenarios' in data and 'total_cenarios' in data:
            if len(data['cenarios']) != data['total_cenarios']:
                self.warnings.append(f"2_cenarios_exportacao.json: total_cenarios não corresponde ao tamanho do array")
    
    def _validate_regras_recepcao(self, data: Dict):
        """Valida arquivo 3_regras_recepcao_dps.json"""
        required_keys = ['titulo', 'versao', 'descricao', 'total_regras', 'regras']
        
        for key in required_keys:
            if key not in data:
                self.errors.append(f"3_regras_recepcao_dps.json: campo '{key}' ausente")
    
    def _validate_leiaute(self, data: Dict):
        """Valida arquivo 4_leiaute_dps_nfse.json"""
        required_keys = ['titulo', 'versao', 'descricao', 'total_campos', 'campos']
        
        for key in required_keys:
            if key not in data:
                self.errors.append(f"4_leiaute_dps_nfse.json: campo '{key}' ausente")
    
    def _validate_regras_validacao(self, data: Dict):
        """Valida arquivo 5_regras_validacao_nfse.json"""
        required_keys = ['titulo', 'versao', 'descricao', 'total_regras', 'regras']
        
        for key in required_keys:
            if key not in data:
                self.errors.append(f"5_regras_validacao_nfse.json: campo '{key}' ausente")
    
    def _validate_data_consistency(self):
        """Valida consistência entre arquivos"""
        print("\n🔗 Validando consistência entre arquivos...")
        
        try:
            # Carregar master index
            master_path = self.directory / '0_MASTER_INDEX.json'
            if not master_path.exists():
                return
            
            with open(master_path, 'r', encoding='utf-8') as f:
                master = json.load(f)
            
            stats = master.get('estatisticas', {})
            
            # Validar totais
            validations = [
                ('1_servicos_incidencia.json', 'servicos', stats.get('total_servicos')),
                ('2_cenarios_exportacao.json', 'cenarios', stats.get('total_cenarios_exportacao')),
                ('3_regras_recepcao_dps.json', 'regras', stats.get('total_regras_recepcao')),
                ('4_leiaute_dps_nfse.json', 'campos', stats.get('total_campos_leiaute')),
                ('5_regras_validacao_nfse.json', 'regras', stats.get('total_regras_validacao'))
            ]
            
            for filename, array_key, expected_total in validations:
                filepath = self.directory / filename
                if not filepath.exists():
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                actual_total = len(data.get(array_key, []))
                
                if actual_total != expected_total:
                    self.warnings.append(
                        f"Inconsistência: {filename} tem {actual_total} registros, "
                        f"mas MASTER_INDEX indica {expected_total}"
                    )
                else:
                    print(f"  ✓ {filename}: {actual_total} registros (consistente)")
        
        except Exception as e:
            self.warnings.append(f"Erro ao validar consistência: {e}")
    
    def _validate_encoding(self):
        """Valida encoding UTF-8"""
        print("\n📝 Validando encoding...")
        
        for filename in self.REQUIRED_FILES:
            filepath = self.directory / filename
            if not filepath.exists():
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    f.read()
                print(f"  ✓ {filename}: UTF-8")
            except UnicodeDecodeError:
                self.errors.append(f"{filename}: encoding não é UTF-8")
    
    def _print_results(self):
        """Imprime resultados da validação"""
        print("\n" + "="*60)
        print("📋 RESULTADOS DA VALIDAÇÃO")
        print("="*60)
        
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("\n✅ SUCESSO! Todos os arquivos estão em conformidade com o padrão.")
        else:
            if self.errors:
                print(f"\n❌ ERROS ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    print(f"  {i}. {error}")
            
            if self.warnings:
                print(f"\n⚠️  AVISOS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
        
        print("\n" + "="*60)


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("❌ Erro: Diretório não especificado")
        print(f"\nUso: python {sys.argv[0]} <diretorio>")
        print(f"\nExemplo: python {sys.argv[0]} output_nfse/")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"❌ Erro: Diretório '{directory}' não encontrado")
        sys.exit(1)
    
    validator = NFSeValidator(directory)
    is_valid = validator.validate()
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
