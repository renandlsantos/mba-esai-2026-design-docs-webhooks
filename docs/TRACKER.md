# TRACKER — inventário e rastreabilidade

## Método e cobertura
Inventário documental revisado: 53 itens da reunião (R01–R53) e 15 itens de integração/refinamento apoiados no código (C01–C15), agrupando repetições da mesma decisão. A revisão manual relacionou os requisitos, decisões e restrições dos documentos a esses 68 itens; **68/68 grupos mapeados (100%)**. O cálculo mede este inventário declarado, não prova automaticamente que nenhum detalhe foi omitido; o leitor pode auditar os grupos e propor desmembramento. **53/68 = 77,94%** das linhas têm fonte TRANSCRICAO (limiar >=70%); **15** referências CODIGO (limiar >=5). Propostas derivadas do código não são decisões ratificadas da reunião.

Fonte da reunião: [TRANSCRICAO.md](../TRANSCRICAO.md). Os timestamps e nomes abaixo são localizadores literais. Propostas técnicas do FDD são identificadas como propostas e não contadas como decisões confirmadas. Q01–Q07 no RFC distinguem contradições, detalhes ausentes e decisões futuras.

| ID | Documento | Tipo | Conteúdo (resumo) | Fonte | Localização |
|---|---|---|---|---|---|
| R01 | [PRD.md](PRD.md) | Problema | Três clientes B2B e polling caro/lento, risco de churn | TRANSCRICAO | [09:00] Marcos |
| R02 | [PRD.md](PRD.md) | Objetivo | Menos de 10s em operação normal | TRANSCRICAO | [09:02] Marcos |
| R03 | [PRD.md](PRD.md) | Escopo | Somente outbound | TRANSCRICAO | [09:02] Marcos |
| R04 | [RFC.md](RFC.md) | Alternativa | Não enviar HTTP síncrono na transação | TRANSCRICAO | [09:04] Bruno |
| R05 | [FDD.md](FDD.md) | Atomicidade | Pedido/histórico/outbox na mesma transação | TRANSCRICAO | [09:06] Diego |
| R06 | [adrs/ADR-001-outbox-mysql.md](adrs/ADR-001-outbox-mysql.md) | Decisão | MySQL existente, rejeitar nova infra Redis | TRANSCRICAO | [09:07] Diego |
| R07 | [FDD.md](FDD.md) | Operação | Índice status/created_at e lote pequeno | TRANSCRICAO | [09:08] Diego |
| R08 | [PRD.md](PRD.md) | Não escopo | Arquivamento após ~30 dias é futuro | TRANSCRICAO | [09:08] Diego |
| R09 | [adrs/ADR-005-worker-polling.md](adrs/ADR-005-worker-polling.md) | Decisão | Polling a cada 2s | TRANSCRICAO | [09:10] Larissa |
| R10 | [RFC.md](RFC.md) | Alternativa | Trigger não notifica processo externo | TRANSCRICAO | [09:09] Diego |
| R11 | [FDD.md](FDD.md) | Execução | Processo separado e entrada worker proposta | TRANSCRICAO | [09:11] Larissa |
| R12 | [FDD.md](FDD.md) | Ordenação | Um worker, ordem por pedido | TRANSCRICAO | [09:12] Diego |
| R13 | [PRD.md](PRD.md) | Limitação | Sem ordem global, multiworker é futuro | TRANSCRICAO | [09:13] Larissa |
| R14 | [adrs/ADR-002-retry-dead-letter.md](adrs/ADR-002-retry-dead-letter.md) | Resiliência | Rejeitar retry indefinido e três tentativas | TRANSCRICAO | [09:15] Diego |
| R15 | [RFC.md](RFC.md) | Pendência | Cinco tentativas e cinco intervalos precisam definição | TRANSCRICAO | [09:17] Larissa |
| R16 | [FDD.md](FDD.md) | Resiliência | DLQ separada com payload, motivo e timestamp | TRANSCRICAO | [09:18] Diego |
| R17 | [FDD.md](FDD.md) | Contrato | POST admin replay reinsere pending | TRANSCRICAO | [09:18] Diego |
| R18 | [adrs/ADR-003-hmac-endpoint.md](adrs/ADR-003-hmac-endpoint.md) | Segurança | Assinar corpo com HMAC-SHA256 | TRANSCRICAO | [09:20] Sofia |
| R19 | [FDD.md](FDD.md) | Segurança | Segredo único por endpoint com url/cliente/ativo | TRANSCRICAO | [09:21] Sofia |
| R20 | [FDD.md](FDD.md) | Segurança | Rotação pela API e chave antiga válida 24h | TRANSCRICAO | [09:21] Sofia |
| R21 | [PRD.md](PRD.md) | Validação | URL HTTPS obrigatória via Zod | TRANSCRICAO | [09:23] Sofia |
| R22 | [FDD.md](FDD.md) | Limite | 64 KB e erro, sem truncamento | TRANSCRICAO | [09:24] Larissa |
| R23 | [adrs/ADR-004-at-least-once.md](adrs/ADR-004-at-least-once.md) | Garantia | At least once, duplicatas possíveis | TRANSCRICAO | [09:24] Diego |
| R24 | [FDD.md](FDD.md) | Idempotência | UUID gerado na outbox, X-Event-Id e dedup cliente | TRANSCRICAO | [09:25] Diego |
| R25 | [RFC.md](RFC.md) | Alternativa | Exactly once descartado por complexidade | TRANSCRICAO | [09:25] Diego |
| R26 | [PRD.md](PRD.md) | Dependência | Documentar garantia no portal dos clientes | TRANSCRICAO | [09:26] Marcos |
| R27 | [adrs/ADR-006-padroes-existentes.md](adrs/ADR-006-padroes-existentes.md) | Estrutura | Módulo controller/service/repository/routes/schemas | TRANSCRICAO | [09:27] Bruno |
| R28 | [FDD.md](FDD.md) | Estrutura | Processador/worker dentro do módulo | TRANSCRICAO | [09:28] Bruno |
| R29 | [FDD.md](FDD.md) | Erros | AppError e prefixo WEBHOOK_ | TRANSCRICAO | [09:29] Larissa |
| R30 | [FDD.md](FDD.md) | Reuso | Pino e middleware AppError/Zod/Prisma | TRANSCRICAO | [09:29] Bruno |
| R31 | [FDD.md](FDD.md) | Infra | PrismaClient separado e mesma DATABASE_URL | TRANSCRICAO | [09:30] Bruno |
| R32 | [PRD.md](PRD.md) | CRUD | Cadastro devolve secret gerada e aceita status | TRANSCRICAO | [09:31] Marcos |
| R33 | [FDD.md](FDD.md) | Correção | customer_id explícito, não inferido do JWT | TRANSCRICAO | [09:32] Larissa |
| R34 | [FDD.md](FDD.md) | CRUD | PATCH, DELETE e GET por cliente | TRANSCRICAO | [09:33] Bruno |
| R35 | [FDD.md](FDD.md) | Filtro | Filtro de status na inserção; nenhum assinante não insere | TRANSCRICAO | [09:34] Bruno |
| R36 | [FDD.md](FDD.md) | Consulta | GET deliveries: últimas100 resultado/payload/response/tempo | TRANSCRICAO | [09:34] Marcos |
| R37 | [FDD.md](FDD.md) | Autorização | Replay ADMIN com identidade auditada e requireRole | TRANSCRICAO | [09:36] Sofia |
| R38 | [PRD.md](PRD.md) | Autorização | CRUD qualquer role autenticada inicialmente | TRANSCRICAO | [09:37] Sofia |
| R39 | [PRD.md](PRD.md) | Não escopo | Fallback por e-mail excluído | TRANSCRICAO | [09:37] Larissa |
| R40 | [RFC.md](RFC.md) | Ponto aberto | Rate limit: observar e decidir depois | TRANSCRICAO | [09:39] Diego |
| R41 | [PRD.md](PRD.md) | Não escopo | Dashboard é projeto separado | TRANSCRICAO | [09:40] Larissa |
| R42 | [FDD.md](FDD.md) | Integração | changeStatus reverte se outbox falhar | TRANSCRICAO | [09:40] Bruno |
| R43 | [FDD.md](FDD.md) | Integração | publishWebhookEvent recebe tx atual | TRANSCRICAO | [09:41] Bruno |
| R44 | [FDD.md](FDD.md) | Timeout | 10s no HTTP; lentidão vira falha/retry | TRANSCRICAO | [09:42] Diego |
| R45 | [FDD.md](FDD.md) | Payload | Campos do evento e sem items | TRANSCRICAO | [09:43] Diego |
| R46 | [FDD.md](FDD.md) | Headers | EventId, Signature, Timestamp envio e Content-Type | TRANSCRICAO | [09:44] Diego |
| R47 | [FDD.md](FDD.md) | Headers | X-Webhook-Id identifica endpoint | TRANSCRICAO | [09:44] Sofia |
| R48 | [PRD.md](PRD.md) | Expectativa | Atlas solicita fim de novembro | TRANSCRICAO | [09:45] Marcos |
| R49 | [RFC.md](RFC.md) | Planejamento | Estimativa três sprints, não prazo garantido | TRANSCRICAO | [09:46] Larissa |
| R50 | [PRD.md](PRD.md) | Revisão | Segurança dois dias úteis antes deploy | TRANSCRICAO | [09:46] Sofia |
| R51 | [RFC.md](RFC.md) | Governança | Revisar design docs antes codificação | TRANSCRICAO | [09:50] Larissa |
| R52 | [FDD.md](FDD.md) | Identificador | UUID segue padrão existente | TRANSCRICAO | [09:51] Larissa |
| R53 | [FDD.md](FDD.md) | Snapshot | Renderizar payload na inserção, não no envio | TRANSCRICAO | [09:52] Larissa |
| C01 | [FDD.md](FDD.md) | Integração | changeStatus usa transação Prisma | CODIGO | `src/modules/orders/order.service.ts` |
| C02 | [FDD.md](FDD.md) | Integração | Router central registra módulos | CODIGO | `src/routes/index.ts` |
| C03 | [FDD.md](FDD.md) | Autorização | JWT tem id/email/role, requireRole disponível | CODIGO | `src/middlewares/auth.middleware.ts` |
| C04 | [FDD.md](FDD.md) | Erros | Envelope AppError/Zod/Prisma e log inesperado | CODIGO | `src/middlewares/error.middleware.ts` |
| C05 | [FDD.md](FDD.md) | Erros | AppError statusCode/errorCode/details | CODIGO | `src/shared/errors/app-error.ts` |
| C06 | [FDD.md](FDD.md) | Dados | OrderNumber string, Customer/Order/histórico e UUIDs | CODIGO | `prisma/schema.prisma` |
| C07 | [FDD.md](FDD.md) | Padrão | Repository encapsula consultas de pedidos | CODIGO | `src/modules/orders/order.repository.ts` |
| C08 | [adrs/ADR-003-hmac-endpoint.md](adrs/ADR-003-hmac-endpoint.md) | Validação | Schemas Zod no módulo de orders | CODIGO | `src/modules/orders/order.schemas.ts` |
| C09 | [adrs/ADR-005-worker-polling.md](adrs/ADR-005-worker-polling.md) | Execução | Entry point HTTP existente serve de padrão | CODIGO | `src/server.ts` |
| C10 | [FDD.md](FDD.md) | Proposta de contrato | Paths/envelopes/códigos CRUD exemplificados seguem padrão de módulos; revisar antes de implementar | CODIGO | `src/modules/orders/order.routes.ts` |
| C11 | [FDD.md](FDD.md) | Proposta de modelo | Relações/UUID/campos novos derivam modelos existentes e requisitos R05/R16/R19 | CODIGO | `prisma/schema.prisma` |
| C12 | [FDD.md](FDD.md) | Proposta de erro | Novos códigos e HTTP propostos seguem AppError; não existem ainda | CODIGO | `src/shared/errors/app-error.ts` |
| C13 | [RFC.md](RFC.md) | Risco derivado | Autorização por cliente precisa revisão porque JWT não contém customer_id | CODIGO | `src/middlewares/auth.middleware.ts` |
| C14 | [FDD.md](FDD.md) | Aceite derivado | Cenários transacionais e contratos futuros derivam changeStatus e requisitos rastreados | CODIGO | `src/modules/orders/order.service.ts` |
| C15 | [FDD.md](FDD.md) | Operação proposta | Logs e correlação reutilizam logger e tratamento de erros existentes | CODIGO | `src/middlewares/error.middleware.ts` |
