# ADR-001 — Outbox no MySQL existente

## Status
Decisão registrada na reunião; formalização documental para revisão em 2026-09-19. Ressalvas apontadas abaixo não estão ratificadas.

## Contexto
A mudança de status altera pedido, histórico e estoque dentro de prisma.$transaction. HTTP síncrono acoplaria a disponibilidade do cliente à transação.

## Decisão
Persistir snapshot e UUID da outbox na mesma transação MySQL. Se falhar a inserção, reverter a mudança. O worker lê após commit.

## Alternativas Consideradas
Enviar HTTP síncrono foi descartado por latência/rollback; Redis Streams exigiria nova infraestrutura sem necessidade inicial.

## Consequências e trade-offs
Atomicidade local elimina lacuna entre commit do pedido e registro do evento. Não assegura exactly once remoto. Exige índices, operação do worker e plano futuro de retenção.

## Evidência e integração
Transcrição: [09:06] Diego; [09:07] Diego; [09:40] Bruno; [09:51] Larissa; [09:52] Larissa. Código existente: [src/modules/orders/order.service.ts](../../src/modules/orders/order.service.ts). O arquivo evidencia o padrão/ponto de integração, não uma implementação de webhooks pronta.
Ver [RFC](../RFC.md), [FDD](../FDD.md) e [TRACKER](../TRACKER.md).
