#!/usr/bin/env python3
"""
Script para importar JSONs do output-source para o banco SQLite.

Uso:
    python scripts/import_json_to_db.py [--source-dir ../output-source/...]
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adiciona o diretório pai ao path para poder importar app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db, engine
from app.models import (
    ServicoORM, RegraORM, CenarioORM, CampoLayoutORM,
    RestricaoORM, MasterIndexORM
)


class JSONImporter:
    """Importa dados dos JSONs para o banco SQLite"""
    
    def __init__(self, source_dir: Path):
        self.source_dir = Path(source_dir)
        self.session = SessionLocal()
        self.stats = {
            "servicos": 0,
            "regras": 0,
            "cenarios": 0,
            "campos": 0,
            "restricoes": 0,
            "erros": []
        }
    
    def run(self):
        """Executa importação completa"""
        print(f"📂 Importando dados de: {self.source_dir}")
        
        if not self.source_dir.exists():
            print(f"❌ Diretório não encontrado: {self.source_dir}")
            return False
        
        try:
            # Cria tabelas
            print("🔨 Criando tabelas...")
            init_db()
            
            # Importa em ordem
            self._import_master_index()
            self._import_servicos()
            self._import_regras()
            self._import_cenarios()
            self._import_campos_layout()
            
            print("\n✅ Importação concluída com sucesso!")
            self._print_stats()
            return True
            
        except Exception as e:
            print(f"\n❌ Erro durante importação: {e}")
            self.stats["erros"].append(str(e))
            return False
        finally:
            self.session.close()
    
    def _import_master_index(self):
        """Importa master index"""
        print("\n📋 Importando master index...")
        
        arquivo = self.source_dir / "0_MASTER_INDEX.json"
        if not arquivo.exists():
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            return
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove registros antigos
        self.session.query(MasterIndexORM).delete()
        
        master = MasterIndexORM(
            versao_leiaute=data.get("versao", "desconhecida"),
            arquivo_origem=data.get("arquivo_origem", ""),
            data_conversao=data.get("data_conversao", datetime.now().isoformat()),
            total_servicos=data.get("estatisticas", {}).get("total_servicos", 0),
            total_regras=data.get("estatisticas", {}).get("total_regras", 0),
            total_cenarios=data.get("estatisticas", {}).get("total_cenarios", 0),
            total_campos=data.get("estatisticas", {}).get("total_campos", 0),
            total_restricoes=0,  # Calcularemos depois
        )
        
        self.session.add(master)
        self.session.commit()
        print("✅ Master index importado")
    
    def _import_servicos(self):
        """Importa serviços de incidência"""
        print("\n🏢 Importando serviços...")
        
        arquivo = self.source_dir / "1_servicos_incidencia.json"
        if not arquivo.exists():
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            return
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove registros antigos
        self.session.query(ServicoORM).delete()
        
        versao = data.get("versao_leiaute", "v1-03-00-2013-nt007")
        servicos = data.get("servicos", [])
        
        for s in servicos:
            try:
                servico = ServicoORM(
                    codigo_tributacao=s.get("codigo_tributacao"),
                    descricao=s.get("descricao", ""),
                    estabelecimento_prestador=s.get("localidade_incidencia", {}).get("estabelecimento_prestador"),
                    local_prestacao=s.get("localidade_incidencia", {}).get("local_prestacao"),
                    estabelecimento_tomador=s.get("localidade_incidencia", {}).get("estabelecimento_tomador"),
                    estabelecimento_emitente=s.get("localidade_incidencia", {}).get("estabelecimento_emitente"),
                    obrigatorio=s.get("grupos_informacao", {}).get("obrigatorio"),
                    info_complementares=s.get("grupos_informacao", {}).get("info_complementares"),
                    versao_leiaute=versao,
                )
                self.session.add(servico)
                self.stats["servicos"] += 1
            except Exception as e:
                self.stats["erros"].append(f"Erro ao importar serviço {s.get('codigo_tributacao')}: {e}")
        
        self.session.commit()
        print(f"✅ {self.stats['servicos']} serviços importados")
    
    def _import_regras(self):
        """Importa regras de validação"""
        print("\n⚖️  Importando regras...")
        
        arquivo = self.source_dir / "5_regras_validacao_nfse.json"
        if not arquivo.exists():
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            return
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove registros antigos
        self.session.query(RegraORM).delete()
        
        versao = data.get("versao_leiaute", "v1-03-00-2013-nt007")
        regras = data.get("regras", [])
        
        for r in regras:
            try:
                regra = RegraORM(
                    numero_regra=r.get("numero"),
                    campo=r.get("campo", ""),
                    regra_negocio=r.get("regra_negocio", ""),
                    codigo_erro=r.get("codigo_erro", ""),
                    mensagem_erro=r.get("mensagem_erro", ""),
                    nivel_regra=r.get("nivel_regra", 1),
                    contexto=r.get("contexto"),
                    exemplay=r.get("example"),
                    versao_leiaute=versao,
                )
                self.session.add(regra)
                self.stats["regras"] += 1
            except Exception as e:
                self.stats["erros"].append(f"Erro ao importar regra {r.get('numero')}: {e}")
        
        self.session.commit()
        print(f"✅ {self.stats['regras']} regras importadas")
    
    def _import_cenarios(self):
        """Importa cenários de exportação"""
        print("\n🌍 Importando cenários...")
        
        arquivo = self.source_dir / "2_cenarios_exportacao.json"
        if not arquivo.exists():
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            return
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove registros antigos
        self.session.query(CenarioORM).delete()
        
        versao = data.get("versao_leiaute", "v1-03-00-2013-nt007")
        cenarios = data.get("cenarios", [])
        
        for c in cenarios:
            try:
                locais = c.get("locais", {})
                cenario = CenarioORM(
                    numero_cenario=c.get("cenario"),
                    endereco_tomador=locais.get("endereco_tomador", "Brasil"),
                    endereco_intermediario=locais.get("endereco_intermediario", "Brasil"),
                    local_prestacao=locais.get("local_prestacao", "Brasil"),
                    imunidade_exportacao=c.get("tributacao", {}).get("imunidade_exportacao_nao_incidencia"),
                    tributacao_issqn=c.get("tributacao", {}).get("tributacao_issqn"),
                    obrigatorio_nbs=str(c.get("info_comex", {}).get("nbs", "")).upper() == "SIM",
                    obrigatorio_pais_resultado=str(c.get("info_comex", {}).get("pais_resultado", "")).upper() == "SIM",
                    descricao=c.get("descricao"),
                    versao_leiaute=versao,
                )
                self.session.add(cenario)
                self.stats["cenarios"] += 1
            except Exception as e:
                self.stats["erros"].append(f"Erro ao importar cenário {c.get('cenario')}: {e}")
        
        self.session.commit()
        print(f"✅ {self.stats['cenarios']} cenários importados")
    
    def _import_campos_layout(self):
        """Importa campos do leiaute XML"""
        print("\n📋 Importando campos do leiaute...")
        
        arquivo = self.source_dir / "4_leiaute_dps_nfse.json"
        if not arquivo.exists():
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            return
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove registros antigos
        self.session.query(CampoLayoutORM).delete()
        self.session.query(RestricaoORM).delete()
        
        versao = data.get("versao_leiaute", "v1-03-00-2013-nt007")
        campos = data.get("campos", [])
        
        for c in campos:
            try:
                campo = CampoLayoutORM(
                    numero_campo=c.get("numero"),
                    caminho_xml=c.get("caminho_xml", ""),
                    nome_campo=c.get("campo", ""),
                    elemento_xml=c.get("elemento", ""),
                    tipo_dado=c.get("tipo", "C"),
                    ocorrencia=c.get("ocorrencia", "0-1"),
                    tamanho_maximo=c.get("tamanho"),
                    descricao=c.get("descricao", ""),
                    observacoes=c.get("observacoes"),
                    versao_leiaute=versao,
                )
                self.session.add(campo)
                self.stats["campos"] += 1
                
                # Importa restrições se existirem
                restricoes = c.get("restricoes", [])
                for r in restricoes:
                    restricao = RestricaoORM(
                        campo=campo,
                        tipo_restricao=r.get("tipo", "lista_valores"),
                        descricao=r.get("descricao", ""),
                        versao_leiaute=versao,
                    )
                    self.session.add(restricao)
                    self.stats["restricoes"] += 1
                    
            except Exception as e:
                self.stats["erros"].append(f"Erro ao importar campo {c.get('numero')}: {e}")
        
        self.session.commit()
        print(f"✅ {self.stats['campos']} campos importados")
        print(f"✅ {self.stats['restricoes']} restrições importadas")
    
    def _print_stats(self):
        """Imprime estatísticas da importação"""
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DE IMPORTAÇÃO")
        print("="*60)
        print(f"✅ Serviços: {self.stats['servicos']}")
        print(f"✅ Regras: {self.stats['regras']}")
        print(f"✅ Cenários: {self.stats['cenarios']}")
        print(f"✅ Campos Leiaute: {self.stats['campos']}")
        print(f"✅ Restrições: {self.stats['restricoes']}")
        
        if self.stats["erros"]:
            print(f"\n⚠️  Erros encontrados ({len(self.stats['erros'])}):")
            for erro in self.stats["erros"][:5]:  # Mostra apenas os 5 primeiros
                print(f"   - {erro}")
            if len(self.stats["erros"]) > 5:
                print(f"   ... e mais {len(self.stats['erros']) - 5} erros")


def main():
    parser = argparse.ArgumentParser(
        description="Importa JSONs do output-source para SQLite"
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default="../output-source/Leiaute-nfse-rtc-v1-03-00-2013-nt007",
        help="Diretório contendo os JSONs a importar"
    )
    
    args = parser.parse_args()
    
    importer = JSONImporter(args.source_dir)
    success = importer.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
