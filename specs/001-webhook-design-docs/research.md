# Research — decisões de preparação

- Usar seis ADRs: cobre as seis decisões centrais solicitadas, sem fragmentar artificialmente cada detalhe. Alternativa: oito ADRs, rejeitada por repetição.
- Preservar aplicação: o desafio exige design docs, portanto não adicionar tabelas/rotas executáveis. Alternativa: implementar webhooks antecipadamente, rejeitada por violar escopo.
- Conferir fonte primária: TRANSCRICAO.md e código versionado. Aulas orientam estrutura, não introduzem requisitos de negócio.
- Não resolver silenciosamente contradições: cinco tentativas e cinco intervalos de backoff são incompatíveis sem definir contagem. RFC/FDD devem manter decisão pendente antes de implementação.
- Ordenação por pedido em falhas e formato de assinatura durante rotação precisam de contrato explícito; não assumir que ORDER BY created_at resolve retries.
- Rastreabilidade: inventário de requisitos identificáveis com IDs estáveis, origem e timestamp/caminho. Medir percentual sobre inventário explicitamente descrito, não sobre frases arbitrárias.
