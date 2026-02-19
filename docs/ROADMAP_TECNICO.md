# Roadmap Tecnico

Base de planejamento: 19 de fevereiro de 2026
Horizonte: 4 a 8 semanas

## 1. Direcionadores

Objetivo tecnico:
- evoluir de MVP funcional local para baseline de producao com qualidade operacional

Principios:
- contratos de API explicitamente tipados
- build/test automatizado antes de merge
- observabilidade minima em todas as operacoes

## 2. Fases

### Fase A - Baseline de Engenharia (prioridade maxima)
Status: em progresso

Entregas:
1. Frontend build estavel
- corrigir `vite.config.ts` para ambiente TypeScript atual
- garantir `npm run build` sem erro

2. Testes backend executaveis
- consolidar execucao de `pytest`
- adicionar cobertura minima e relatorio simples

3. CI/CD inicial
- criar workflow GitHub Actions com:
  - instalacao dependencias
  - lint/build frontend
  - testes backend

Criterio de pronto:
- pipeline verde em branch principal

### Fase B - Contratos e Robustez da API
Status: nao iniciado

Entregas:
1. Padronizar respostas
- remover respostas genericas restantes (`dict`)
- padronizar envelope de erro em todo backend

2. Hardening de validacao
- revisar filtros e limites de query
- garantir mensagens de erro claras e rastreaveis

3. Testes de integracao
- cobrir rotas criticas: busca, regras por filtro, comparacao de cenarios

Criterio de pronto:
- contratos estaveis com testes de regressao

### Fase C - Seguranca e Operacao
Status: nao iniciado

Entregas:
1. Seguranca
- autenticacao/autorizacao
- rate limiting
- revisao de CORS por ambiente

2. Operacao
- estrategia de deploy
- checklists de release
- politicas de logs por ambiente

3. Observabilidade evoluida
- metricas de disponibilidade e latencia
- monitoramento externo

Criterio de pronto:
- ambiente de homologacao com controles minimos de seguranca

## 3. Backlog Priorizado (curto prazo)

1. Corrigir build TypeScript frontend
2. Configurar workflow CI
3. Cobrir testes automatizados de busca
4. Eliminar `response_model=dict` de rotas restantes
5. Definir politica de versionamento de API

## 4. Riscos do Roadmap

- divergencia entre contrato backend e consumo frontend
- ausencia de CI atrasando deteccao de regressao
- acoplamento a SQLite para cenarios de maior carga

Mitigacao:
- adotar testes de contrato
- travar merge com pipeline obrigatorio
- planejar caminho para banco de producao quando necessario

## 5. Metricas de acompanhamento

- Taxa de sucesso do pipeline CI
- Tempo medio de resposta por endpoint critico
- Quantidade de regressao por sprint
- Cobertura de testes backend/frontend

## 6. Marco de revisao

- Revisao semanal do roadmap com status por item
- Ajustes por evidencia (falha de build, bug recorrente, bloqueio de deploy)
