# ADR-006 — Reutilizar padrões e infraestrutura da aplicação

## Status
Decisão registrada na reunião; formalização documental para revisão em 2026-09-19. Ressalvas apontadas abaixo não estão ratificadas.

## Contexto
Código já possui módulos controller/service/repository/routes/schema, AppError, middleware central, Pino e Prisma.

## Decisão
Novo módulo webhooks segue essas convenções, valida com Zod, usa prefixo WEBHOOK_, reutiliza authenticate/requireRole e logger; worker cria cliente Prisma por processo.

## Alternativas Consideradas
Criar framework, logger ou camada de erro paralelos aumentaria manutenção sem necessidade (alternativa técnica analisada, não decisão literal da reunião).

## Consequências e trade-offs
Reduz divergência de contratos e facilita revisão. Não implica reusar a mesma instância de Prisma entre processos. Pontos de extensão reais constam do FDD.

## Evidência e integração
Transcrição: [09:27] Bruno; [09:28] Bruno; [09:29] Larissa; [09:30] Larissa. Código existente: [src/middlewares/error.middleware.ts](../../src/middlewares/error.middleware.ts). O arquivo evidencia o padrão/ponto de integração, não uma implementação de webhooks pronta.
Ver [RFC](../RFC.md), [FDD](../FDD.md) e [TRACKER](../TRACKER.md).
