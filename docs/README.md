# Documentacao do Projeto NFSe Leiaute

Este diretorio concentra a documentacao oficial do projeto `leiaute-nfse-web`.

## Objetivo do Projeto

Construir um portal para consulta e analise do leiaute NFSe, com foco em:
- consulta de servicos, regras e cenarios
- busca textual unificada
- apoio a validacao funcional e tecnica
- base para evolucao para um produto operavel em producao

## Escopo Atual

- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: React + TypeScript + Vite
- Dados carregados localmente no banco `nfse_leiaute.db`
- API com rotas de servicos, regras, cenarios, busca e health

## Estrutura desta Pasta

1. `STATUS_ATUAL.md`
   Visao executiva do estado atual (arquitetura, modulos, status tecnico).

2. `AVANCOS_IMPLEMENTADOS.md`
   Registro consolidado do que ja foi implementado no ciclo atual.

3. `ROADMAP_TECNICO.md`
   Plano de evolucao por fases com prioridades, entregas e criterio de pronto.

4. `RELATORIO_DIFICULDADES_API.md`
   Problemas conhecidos, riscos, causas provaveis e mitigacoes.

5. `TROUBLESHOOTING_RAPIDO.md`
   Runbook pratico para diagnostico e recuperacao rapida.

6. `LICOES_APRENDIDAS.md`
   Decisoes e aprendizados tecnicos para orientar proximas implementacoes.

## Como Usar

- Para entender o estado do projeto: leia `STATUS_ATUAL.md`
- Para planejar execucao: leia `ROADMAP_TECNICO.md`
- Para executar manutencao: use `TROUBLESHOOTING_RAPIDO.md`
- Para onboarding de dev: leia `STATUS_ATUAL.md` + `LICOES_APRENDIDAS.md`

## Convencoes

- Todas as datas devem usar formato absoluto (ex.: 19 de fevereiro de 2026)
- Status de item deve usar: `nao iniciado`, `em progresso`, `concluido`
- Nao registrar metricas sem fonte clara (comando, log, teste ou consulta)

## Revisao

- Ultima revisao: 19 de fevereiro de 2026
- Proxima revisao sugerida: ao final da proxima sprint tecnica
