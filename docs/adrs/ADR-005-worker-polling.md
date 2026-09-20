# ADR-005 — Worker separado com polling de 2 segundos

## Status
Decisão registrada na reunião; formalização documental para revisão em 2026-09-19. Ressalvas apontadas abaixo não estão ratificadas.

## Contexto
API e entrega têm ciclos de vida distintos. MySQL não fornece o canal NOTIFY/LISTEN sugerido no debate.

## Decisão
Processo Node separado, entrada proposta src/worker.ts, polling a cada 2s, PrismaClient próprio no mesmo banco, inicialmente um worker e ordem por pedido.

## Alternativas Consideradas
HTTP no processo da API foi rejeitado pelo acoplamento; trigger notificando processo externo exigiria mecanismo improvisado.

## Consequências e trade-offs
Isola execução e reutiliza infraestrutura; polling e duração das chamadas influenciam latência. Sem ordem global; escalabilidade futura exige particionamento/locks. Ordenação em retry depende Q02.

## Evidência e integração
Transcrição: [09:09] Diego; [09:10] Larissa; [09:11] Diego; [09:12] Diego; [09:13] Larissa; [09:30] Bruno. Código existente: [src/server.ts](../../src/server.ts). O arquivo evidencia o padrão/ponto de integração, não uma implementação de webhooks pronta.
Ver [RFC](../RFC.md), [FDD](../FDD.md) e [TRACKER](../TRACKER.md).
