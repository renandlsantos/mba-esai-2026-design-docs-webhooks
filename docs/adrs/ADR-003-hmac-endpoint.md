# ADR-003 — HMAC-SHA256 por endpoint

## Status
Decisão registrada na reunião; formalização documental para revisão em 2026-09-19. Ressalvas apontadas abaixo não estão ratificadas.

## Contexto
Clientes precisam verificar origem e integridade; um segredo global ampliaria o impacto de vazamento.

## Decisão
Assinar corpo com HMAC-SHA256, segredo único por endpoint, HTTPS obrigatório e rotação por API com validade simultânea da chave antiga por 24h.

## Alternativas Consideradas
Segredo global foi rejeitado pelo impacto de comprometimento; ausência de assinatura não atende à verificação de origem.

## Consequências e trade-offs
Isola segredo por cadastro e permite transição. Encoding/cabeçalhos de rotação e distribuição da nova chave dependem Q03. Não inventar dupla assinatura como decisão da reunião. Implementação deve reutilizar validação Zod e passar por revisão de Segurança.

## Evidência e integração
Transcrição: [09:20] Sofia; [09:21] Sofia; [09:22] Sofia; [09:23] Sofia. Código existente: [src/modules/orders/order.schemas.ts](../../src/modules/orders/order.schemas.ts). O arquivo evidencia o padrão/ponto de integração, não uma implementação de webhooks pronta.
Ver [RFC](../RFC.md), [FDD](../FDD.md) e [TRACKER](../TRACKER.md).
