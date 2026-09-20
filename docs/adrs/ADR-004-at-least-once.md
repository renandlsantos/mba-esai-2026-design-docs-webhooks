# ADR-004 — At least once e deduplicação por UUID

## Status
Decisão registrada na reunião; formalização documental para revisão em 2026-09-19. Ressalvas apontadas abaixo não estão ratificadas.

## Contexto
Falha após envio e antes de persistência local permite envio duplicado. Exatamente uma vez exigiria coordenação com todos os receptores.

## Decisão
Garantia at least once; UUID criado na inserção da outbox e enviado em X-Event-Id. Consumidor deduplica por event_id; snapshot permanece estável.

## Alternativas Consideradas
Exactly once foi descartado por coordenação/complexidade adicional. At most once arriscaria perda de notificação (análise técnica, não opção debatida na reunião).

## Consequências e trade-offs
Cliente assume deduplicação e precisa de documentação. Replay preservando UUID é proposta pendente Q07, não decisão expressa. UUID segue padrão existente.

## Evidência e integração
Transcrição: [09:24] Diego; [09:25] Diego; [09:26] Larissa; [09:51] Larissa. Código existente: [prisma/schema.prisma](../../prisma/schema.prisma). O arquivo evidencia o padrão/ponto de integração, não uma implementação de webhooks pronta.
Ver [RFC](../RFC.md), [FDD](../FDD.md) e [TRACKER](../TRACKER.md).
