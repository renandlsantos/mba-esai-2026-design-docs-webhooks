# ADR-002 — Retry e dead letter separada

## Status
Decisão registrada na reunião; formalização documental para revisão em 2026-09-19. Ressalvas apontadas abaixo não estão ratificadas.

## Contexto
Receptores podem ficar indisponíveis por horas; três tentativas rápidas não cobrem manutenção e retries infinitos deixam pendências sem fim.

## Decisão
Registrar backoff 1m/5m/30m/2h/12h, dead letter separada com payload/motivo/data e replay administrativo. A referência a cinco tentativas exige esclarecimento Q01 antes de codificar o contador.

## Alternativas Consideradas
Três tentativas e retry indefinido foram descartados; marcar falha na mesma outbox foi alternativa à tabela separada.

## Consequências e trade-offs
Facilita diagnóstico/reprocessamento, com custo de tabelas e auditoria. Replay exige ADMIN. Q01 e ordenação durante retry (Q02) permanecem pendentes; calendário não foi arbitrariamente corrigido.

## Evidência e integração
Transcrição: [09:15] Diego; [09:16] Bruno; [09:17] Larissa; [09:18] Diego; [09:36] Sofia. Código existente: [src/middlewares/auth.middleware.ts](../../src/middlewares/auth.middleware.ts). O arquivo evidencia o padrão/ponto de integração, não uma implementação de webhooks pronta.
Ver [RFC](../RFC.md), [FDD](../FDD.md) e [TRACKER](../TRACKER.md).
