# Relatorio de Dificuldades e Riscos da API

Data: 19 de fevereiro de 2026

Este documento consolida problemas recorrentes, causas provaveis e mitigacoes praticas.

## 1. Problemas Conhecidos Atuais

### 1.1 Divergencia de contrato (busca)
Sintoma:
- frontend tentando ler `items` quando backend retorna `resultados`

Impacto:
- erro de runtime no cliente

Mitigacao aplicada:
- normalizacao no client frontend (`api.search`)

Mitigacao definitiva recomendada:
- padronizar definitivamente o contrato da rota de busca no backend

### 1.2 Build TypeScript quebrando no frontend
Sintoma:
- erro em `vite.config.ts` relacionado a `path` e `__dirname`

Impacto:
- bloqueio de build para release

Mitigacao recomendada:
- alinhar configuracao de tipos Node no projeto Vite

### 1.3 Ausencia de CI/CD
Sintoma:
- validacao manual de qualidade

Impacto:
- regressao pode chegar na branch principal

Mitigacao recomendada:
- workflow minimo com build frontend + testes backend

## 2. Riscos Tecnicos

1. Risco de contrato instavel entre API e UI
- Probabilidade: media
- Severidade: alta
- Acao: testes de contrato + schemas explicitos

2. Risco de observabilidade incompleta
- Probabilidade: media
- Severidade: media
- Acao: evoluir logging para metrics/alertas

3. Risco de escalabilidade com SQLite
- Probabilidade: baixa no curto prazo
- Severidade: media/alta no medio prazo
- Acao: planejar migracao para banco orientado a producao quando houver demanda

## 3. Causas Raiz recorrentes

- tipagem frouxa em contratos de API
- historico de respostas genericas (`dict`) em algumas rotas
- ausencia de gate automatico antes de merge

## 4. Plano de Mitigacao (ordem sugerida)

1. Fechar pipeline CI basico
2. Padronizar respostas de todas as rotas
3. Cobrir fluxo de busca com testes automatizados
4. Definir checklist de release tecnico

## 5. Criterios de Saida deste Relatorio

Considerar estes riscos controlados quando:
- build frontend estiver verde em CI
- testes backend executarem automaticamente
- nenhuma rota de negocio retornar contrato ambiguo
