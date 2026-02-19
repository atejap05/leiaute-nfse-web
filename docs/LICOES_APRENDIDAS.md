# Licoes Aprendidas

Consolidacao tecnica ate 19 de fevereiro de 2026.

## 1. Licoes de Arquitetura

1. Contratos explicitos vencem rapidez de curto prazo
- rotas com resposta generica aumentam risco de regressao no frontend
- schemas especificos reduzem ambiguidade e aceleram debug

2. Tipagem precisa refletir dado real
- dados legados exigem campos nullable/unioes
- ignorar isso quebra validacao e serializacao

3. Middleware de observabilidade vale desde o inicio
- `request_id` + latencia por request simplificam suporte

## 2. Licoes de Integracao Backend-Frontend

1. API e cliente precisam compartilhar convencoes de payload
- divergencia `resultados` vs `items` gerou erro em producao local

2. Normalizacao defensiva no client evita quebra de UX
- mesmo com backend correto, fallback no client reduz impacto de variacoes

3. Erro padronizado acelera tratativa no frontend
- envelope unico para erro simplifica exibicao de mensagens

## 3. Licoes de Processo

1. Sem CI, regressao passa facil
- validacao manual nao escala

2. Documentacao precisa seguir o estado real do codigo
- documentacao divergente gera decisao errada de prioridade

3. Historico deve separar fato de plano
- implementado e planejado devem ser secos e nao misturados

## 4. Antipadroes identificados

- usar `dict` generico como contrato principal de API
- assumir que campo sempre existe no frontend sem fallback
- considerar projeto pronto sem build/test automatizado

## 5. Regras para proximos ciclos

1. Toda nova rota deve ter schema de resposta
2. Toda mudanca de contrato deve atualizar client e testes
3. Nenhum merge sem validacao automatica minima
4. Toda incidencia relevante deve gerar atualizacao em `docs/`

## 6. Proximas acoes recomendadas

- completar padronizacao de contratos na busca auxiliar
- resolver build TypeScript do frontend
- ativar CI com lint/build/test
- criar guia de contribuicao para novos devs
