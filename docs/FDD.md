# FDD — Webhooks outbound

**Status:** desenho para revisão, sem implementação de runtime. Decisões confirmadas pela reunião são chamadas de requisitos; detalhes técnicos adicionais são marcados **proposta** e dependem de ratificação. Fontes no [TRACKER](TRACKER.md).

## Contexto e motivação técnica
A aplicação atual não notifica sistemas externos. A mudança de status já é transacional; a outbox estende essa garantia local sem colocar HTTP na transação (R04–R06/C01 no tracker).

## Objetivos técnicos
Persistir snapshot atomicamente, entregar de forma desacoplada, suportar repetição/deduplicação e permitir diagnóstico/replay com padrões existentes. Este documento especifica os pontos conhecidos e torna visíveis decisões ainda não fechadas.

## Escopo e exclusões
Inclui desenho de outbox, worker, cadastro, assinatura, retry, dead letter e contratos. Exclui implementação neste desafio, entrada de webhooks, e-mail, dashboard, arquivamento e múltiplos workers, conforme PRD. Detalhes novos são propostas derivadas dos padrões existentes e sujeitos a revisão, não requisitos inventados atribuídos à reunião.

## Integração com o sistema existente
| Arquivo existente | Responsabilidade atual | Alteração futura proposta |
|---|---|---|
| `src/modules/orders/order.service.ts` | OrderService.changeStatus usa prisma.$transaction, altera estoque/pedido/histórico | Chamar publishWebhookEvent(tx, order, fromStatus, toStatus) dentro da mesma transação, após histórico e antes de retorno |
| `src/modules/orders/order.repository.ts` | Consultas de pedidos com filtros | Reutilizar convenções; não fazer HTTP no repository |
| `src/routes/index.ts` | buildApiRouter registra módulos existentes | Registrar router de webhooks e rota administrativa de replay |
| `src/middlewares/auth.middleware.ts` | authenticate verifica JWT de operador; requireRole restringe roles | CRUD autenticado; replay requireRole('ADMIN'); nunca derivar customer_id do JWT |
| `src/middlewares/error.middleware.ts` | Trata AppError, Zod e Prisma; loga erro inesperado | Reutilizar; erros de domínio com prefixo WEBHOOK_ |
| `src/shared/errors/app-error.ts` | AppError(message, statusCode, errorCode, details?) | Usar estrutura existente para erros de cadastro/replay |
| `prisma/schema.prisma` | MySQL, UUIDs e relações Order/Customer/OrderStatusHistory | Adicionar modelos de endpoint, assinatura, outbox, tentativa e dead letter sem alterar semântica de pedidos |

Arquivos novos **propostos**, ainda inexistentes: `src/worker.ts`, `src/modules/webhooks/webhook.controller.ts`, `webhook.service.ts`, `webhook.repository.ts`, `webhook.routes.ts`, `webhook.schemas.ts`, `webhook.worker.ts` e `webhook.processor.ts`. Seguir organização controller/service/repository/routes/schema; manter lógica de assinatura e calendário de retry testáveis sem rede.

## Modelo persistido proposto
| Entidade | Campos essenciais propostos | Restrições e índices propostos |
|---|---|---|
| WebhookEndpoint | id UUID, customer_id, url, active, secret_current, secret_previous, previous_valid_until | HTTPS, cliente existente; segredo nunca em listagem/log; tratamento criptográfico em repouso a definir na revisão de segurança |
| WebhookSubscription | endpoint_id, status | Par único; status pertence a OrderStatus existente |
| WebhookOutbox | id UUID, endpoint_id, order_id, payload_snapshot, status, created_at, next_attempt_at, attempts | Snapshot imutável; índice status/created_at solicitado; índice de vencimento conforme consulta após decisão Q02 |
| WebhookDelivery | id, event_id, endpoint_id, attempted_at, status_code, response, duration_ms, error | Registro por tentativa; limite de tamanho de response ainda a definir |
| WebhookDeadLetter | id, event_id, endpoint_id, payload, reason, failed_at | Tabela separada; preserve dados para replay e auditoria |
| ReplayAudit | id, dead_letter_id, operator_id, replayed_at | Proposta de trilha de identidade exigida pela reunião |

Estados propostos da outbox: pending → processing → delivered; em falha processing → pending com next_attempt_at; esgotamento → dead letter. Claim/lease e recuperação após crash precisam ser implementados de forma transacional para evitar evento preso em processing. Não prometer exactly once: mesmo com claim, crash após entrega antes do commit permite duplicata.

## Fluxo transacional de publicação
1. OrderService.changeStatus inicia a transação existente e valida transição/estoque.
2. Atualiza Order e OrderStatusHistory como no código-base.
3. Consulta endpoints ativos do customer_id cujo filtro inclui to_status. Sem assinante, não grava evento.
4. Constrói snapshot com campos abaixo e UUID; valida tamanho serializado antes de persistir. Snapshot não é reconstruído no worker.
5. Insere outbox no mesmo tx. Erro em qualquer etapa reverte pedido, histórico, estoque e outbox. O erro por tamanho não pode truncar conteúdo; impacto de rejeitar a transação inteira deve constar do contrato final de changeStatus.
6. Commit disponibiliza evento ao worker. Nenhuma chamada de rede é feita dentro da transação.

## Worker e resiliência
O processo proposto `src/worker.ts`, iniciado por `npm run worker`, cria PrismaClient próprio com a mesma DATABASE_URL. A cada 2s busca lote por created_at. O tamanho do lote e a política de lease são parâmetros técnicos a definir, não números citados na reunião. Inicialmente apenas um worker. Envia POST HTTPS com timeout de 10s e persiste tentativa/resultado.

A ordem por pedido deve incluir falhas: apenas ordenar eventos disponíveis por created_at pode deixar um evento mais novo ultrapassar outro em retry. **Q02 bloqueia implementação:** proposta é bloquear posteriores do mesmo pedido/endpoint até decisão do anterior, com documentação do impacto de dead letter. Pedidos diferentes podem progredir; isso não estabelece ordem global.

A sequência registrada é 1m, 5m, 30m, 2h, 12h, mas há referência a cinco tentativas. **Q01 bloqueia calendário definitivo:** cinco intervalos normalmente significam seis envios contando o inicial. Não remover intervalo ou aumentar tentativas silenciosamente. Testes finais devem usar a decisão ratificada.

Após esgotamento, mover para dead letter com payload, motivo e data. Replay ADMIN reinsere pending e audita operador. **Proposta:** preservar event_id e snapshot para permitir deduplicação e manter vínculo com dead letter; política para replay repetido deve ser definida (Q07). Interrupção do processo durante claim/envio/persistência precisa de testes; não apagar histórico automaticamente.

## Contrato outbound
Método POST na URL HTTPS cadastrada. Content-Type: application/json. Payload de exemplo (valores ilustrativos):
```json
{
  "event_id": "6c71baea-630d-4d4a-8e52-9e8f552ca18d",
  "event_type": "order.status_changed",
  "timestamp": "2026-09-19T15:00:00.000Z",
  "order_id": "ff410f33-d635-4a96-9f6a-9bac6a2ec31a",
  "order_number": "ORD-000123",
  "from_status": "PENDING",
  "to_status": "PAID",
  "customer_id": "80d6c1b8-cf3d-4ea3-a2bd-cf543c873316",
  "total_cents": 15990
}
```
Sem itens. order_number é string, coerente com Order.orderNumber String @db.VarChar(20) no schema existente; o exemplo não altera o tipo persistido. Headers obrigatórios: X-Event-Id (UUID), X-Signature (HMAC-SHA256 do payload), X-Timestamp (timestamp do envio), X-Webhook-Id e Content-Type.

A reunião não fixa encoding/prefixo de X-Signature, se X-Timestamp participa do material assinado, unidade de timestamp ou tolerância a replay. **Proposta para revisão de Segurança:** assinar bytes exatos do corpo, documentar encoding e comparação constante, rejeitar corpo alterado e manter contrato de rotação compatível. Não apresentar um exemplo de assinatura como aprovado sem Q03 resolvida. Rotação mantém segredo anterior por 24h; definir entrega da nova chave e verificação de ambas antes de implementar.

Limite de 64 KB: requisito da reunião. **Proposta de precisão:** 65.536 bytes UTF-8, não caracteres; ratificar convenção KB/KiB. Rejeitar excedente, nunca truncar. Timeouts e classificação de respostas: **proposta** considerar 2xx sucesso, erros de rede/timeout e respostas não-2xx falha; detalhes de 3xx/4xx/429 precisam de Q07, inclusive redirecionamento não automático para preservar controle do destino.

## Contratos públicos de administração
Somente paths de deliveries e replay foram explicitamente definidos na reunião; os demais abaixo são propostas seguindo o padrão do projeto. Corpo/resposta/códigos concretos também são propostas para revisão.

| Método/path | Entrada | Resposta proposta | Autorização |
|---|---|---|---|
| POST /webhooks | customer_id, url HTTPS, statuses[], active | 201 com id e secret somente no cadastro | authenticate |
| GET /webhooks | customer_id opcional conforme escopo autorizado | 200 lista sem segredos | authenticate |
| PATCH /webhooks/:id | url, statuses, active; rotação em contrato separado a definir | 200 representação pública | authenticate |
| POST /webhooks/:id/rotate-secret | id | 200 com novo secret, antigo válido por 24h; contrato de assinatura Q03 | authenticate |
| DELETE /webhooks/:id | id | 204; proposta de desativação lógica para preservar entregas | authenticate |
| GET /webhooks/:id/deliveries | id | 200 até 100 últimas tentativas: resultado/payload/resposta/tempo | authenticate |
| POST /admin/webhooks/dead-letter/:id/replay | id | 202 com event_id e estado pending | authenticate + requireRole('ADMIN') |

A identidade do operador é AuthUser.id. customer_id é corpo/path conforme decisão [09:32], nunca claim inexistente. Controle de acesso por cliente é Q06: autenticação isolada não estabelece autorização multi-tenant.

### Exemplos de request/response
Os exemplos abaixo concretizam os contratos propostos, com identificadores fictícios e segredo substituído por texto demonstrativo. Não são respostas de API executada. Os paths de CRUD seguem o padrão de módulos existente; foram especificados aqui para revisão.

**Cadastro — POST /webhooks → 201**
```json
{"customer_id":"80d6c1b8-cf3d-4ea3-a2bd-cf543c873316","url":"https://cliente.example/webhooks","statuses":["SHIPPED","DELIVERED"],"active":true}
```
```json
{"id":"e87ecba3-0359-477a-9ae0-76c0369f22c3","customer_id":"80d6c1b8-cf3d-4ea3-a2bd-cf543c873316","url":"https://cliente.example/webhooks","statuses":["SHIPPED","DELIVERED"],"active":true,"secret":"SEGREDO_GERADO_EXIBIDO_UMA_VEZ"}
```
**Edição — PATCH /webhooks/e87ecba3-0359-477a-9ae0-76c0369f22c3 → 200**
```json
{"statuses":["DELIVERED"],"active":false}
```
```json
{"id":"e87ecba3-0359-477a-9ae0-76c0369f22c3","statuses":["DELIVERED"],"active":false}
```
**Listagem — GET /webhooks?customer_id=80d6c1b8-cf3d-4ea3-a2bd-cf543c873316 → 200**
Request sem corpo; o parâmetro filtra cliente dentro do escopo autorizado a definir.
```json
{"items":[{"id":"e87ecba3-0359-477a-9ae0-76c0369f22c3","url":"https://cliente.example/webhooks","statuses":["DELIVERED"],"active":false}]}
```
**Replay — POST /admin/webhooks/dead-letter/83b45dd5-d130-4147-aa12-5c62f6b30f08/replay → 202**
Request sem corpo; header Authorization contém JWT de ADMIN (não mostrado).
```json
{"event_id":"6c71baea-630d-4d4a-8e52-9e8f552ca18d","status":"pending"}
```
**Rotação — POST /webhooks/e87ecba3-0359-477a-9ae0-76c0369f22c3/rotate-secret → 200**
Request sem corpo. Formato proposto, dependente de Q03.
```json
{"secret":"NOVO_SEGREDO_EXIBIDO_UMA_VEZ","previous_valid_until":"2026-09-20T15:00:00.000Z"}
```
**Entregas — GET /webhooks/e87ecba3-0359-477a-9ae0-76c0369f22c3/deliveries → 200**
Request sem corpo. Exemplo de lista vazia:
```json
{"items":[]}
```
Quando há tentativa, cada item contém event_id, attempted_at, success, payload (objeto outbound completo), response (status_code e body) e duration_ms, conforme a consulta exigida. Os tipos, envelope de listagem e códigos concretos são propostas ancoradas no padrão HTTP atual, não decisões literais da reunião.

## Erros e validação
Reutilizar Zod para formato e HTTPS e AppError para domínio, preservando o envelope do middleware `error: {code, message, details}`. **Códigos propostos**, não inventário existente:

| Código | HTTP proposto | Situação |
|---|---|---|
| WEBHOOK_NOT_FOUND | 404 | Endpoint inexistente |
| WEBHOOK_CUSTOMER_NOT_FOUND | 404 | Cliente inexistente |
| WEBHOOK_INVALID_URL | 400 | URL não HTTPS ou destino rejeitado pela política ratificada |
| WEBHOOK_INVALID_STATUS | 400 | Status fora do conjunto permitido |
| WEBHOOK_PAYLOAD_TOO_LARGE | 422 | Snapshot supera limite; sem truncamento |
| WEBHOOK_DEAD_LETTER_NOT_FOUND | 404 | Replay de registro inexistente |
| WEBHOOK_REPLAY_CONFLICT | 409 | Replay incompatível com estado/política ratificada |

Autenticação e autorização mantêm erros existentes. Timeout de receptor é falha de entrega persistida, não 500 da requisição que já alterou o pedido. Erros internos não retornam segredo nem stack ao cliente.

## Observabilidade e operação
Logs estruturados Pino com event_id, endpoint_id, order_id, tentativa, duração, resultado e trace/correlation id quando disponível. Não registrar segredo nem assinatura como substituto de auditoria. Métricas propostas: idade do pending mais antigo, latência de primeira tentativa, latência de entrega, taxa de sucesso/falha, tentativas e tamanho da dead letter. Limiar de alerta, retenção de payload/resposta e rate limit permanecem abertos. Audit trail de replay inclui operador e referência da dead letter. Segurança revisa dois dias úteis antes de deploy; nenhuma execução está pronta para produção por existir este desenho.

## Dependências, riscos e aceitação técnica
Depende dos modelos Customer/Order e transação Prisma existentes, do cadastro de assinantes e de receptores capazes de deduplicar UUID/verificar HMAC. Antes de migrar/implementar resolver Q01–Q03, Q06–Q07 do RFC. Q04/Q05 exigem acompanhamento operacional. Não há dependência nova Redis ou serviço de fila.

| Teste planejado | Evidência de aceite futura |
|---|---|
| Rollback após inserção da outbox | Pedido/histórico/estoque/evento todos revertidos |
| Commit e ausência de assinantes | Evento somente para clientes/status ativos; nenhum sem assinante |
| Snapshot após mudanças posteriores | Corpo enviado idêntico ao persistido |
| Falha entre POST e persistência | Duplicata mantém UUID, consumidor pode deduplicar |
| Retry e esgotamento | Relógio controlado verifica calendário ratificado e dead letter |
| Dois eventos do mesmo pedido | Política ratificada de ordenação respeitada durante falha |
| Payload multibyte no limite | Validação usa bytes e não trunca |
| HMAC, rotação e timeout | Corpo adulterado rejeitado, 24h conforme contrato e chamada limitada a 10s |
| Roles e replay | Operador negado no replay, ADMIN auditado, UUID conforme decisão |
| Consulta de entregas | Até 100 últimas com ordem determinística e sem segredos |

Testes acima são especificações, não resultados executados. Nesta entrega, scripts/validate_docs.py valida somente documentos, links, fontes e preservação da base.
