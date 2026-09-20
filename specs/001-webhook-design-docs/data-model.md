# Modelo documental

## Requisito
ID estável, resumo, tipo, documento de destino, fonte TRANSCRICAO ou CODIGO e localização verificável. Cada requisito do inventário deve ter pelo menos uma linha no TRACKER.

## Decisão arquitetural
ADR com título, status, contexto, decisão, alternativa, consequências e referência ao código existente. Seis registros relacionados ao RFC/FDD.

## Ponto aberto
Pergunta, evidência de ausência ou conflito, responsável sugerido e impacto/bloqueio. Não deve aparecer como decisão aprovada em outro documento.

## Modelo de domínio proposto (não migrado)
Endpoint pertence a Customer; assinatura de status filtra eventos de Order. Outbox contém snapshot e UUID do evento. Tentativa de entrega referencia evento e endpoint. Dead letter preserva payload e motivo e pode originar replay auditado. O FDD descreve campos e estados sem alterar prisma/schema.prisma.
