# PRD — Notificações de mudança de status de pedidos

**Status:** proposta documental para revisão. **Autor:** Renan Santos, com assistência do Codex. **Data:** 2026-09-19.
**Fonte primária:** [reunião](../TRANSCRICAO.md); decisões e evidências em [TRACKER](TRACKER.md).

## Contexto e problema
Atlas Comercial, MaxDistribuição e Nova Cargo integram com a API de pedidos via polling de GET /orders. A consulta repetitiva aumenta tráfego, custo de integração e atraso percebido. Atlas manifestou risco de cancelamento no fim do trimestre ([09:00] Marcos). O pedido de disponibilidade no fim de novembro é uma expectativa registrada na reunião, não um prazo acadêmico nem um compromisso de implantação desta entrega.

## Público-alvo e cenários de uso
Clientes B2B precisam receber mudanças de status sem consultar continuamente a API. Operadores autenticados administram endpoints de um cliente; administradores recuperam entregas esgotadas. Plataforma opera o worker e Segurança revisa assinatura/rotação. O JWT identifica o operador, não o cliente: customer_id é explícito na requisição.

## Objetivos e métricas
- Notificar mudanças em menos de 10 segundos em condições normais, conforme tolerância do produto ([09:02]); medir latência entre criação do evento e primeira tentativa/entrega, sem confundir polling de 2 segundos com garantia fim a fim.
- Reduzir polling pelos três clientes iniciais. Baseline de consultas e meta percentual ainda precisam ser coletados/ratificados pelo PM; não há percentual na reunião.
- Evitar perda de eventos quando a transação de mudança de status confirma. Verificar atomicidade pedido/histórico/outbox por testes de commit e rollback.
- Permitir investigação e recuperação: medir entregas bem-sucedidas, retries, dead letters e replay auditado. Limiares operacionais de alerta são pendentes de definição.

## Escopo funcional
1. Registrar endpoint com URL HTTPS, customer_id, status assinados e ativo; gerar segredo por endpoint e retorná-lo no cadastro. Listar, atualizar e remover endpoints. Qualquer usuário autenticado pode executar CRUD conforme decisão da reunião; confirmar autorização por cliente antes de exposição multi-tenant é risco em aberto, não comportamento implementado.
2. Publicar somente mudanças de status e somente para assinantes elegíveis. Sem assinante, não gerar evento. Não incluir itens: o receptor consulta GET /orders para detalhes.
3. Na mesma transação de pedido e histórico, salvar outbox com UUID e snapshot do payload. Entrega at least once e deduplicação pelo receptor usando X-Event-Id.
4. Executar worker separado, polling a cada 2 segundos, lote por created_at, com ordenação por pedido e sem garantia global. Inicialmente um worker.
5. Fazer POST HTTPS com timeout de 10 segundos e HMAC-SHA256 por endpoint. Cabeçalhos X-Event-Id, X-Signature, X-Timestamp, X-Webhook-Id e Content-Type.
6. Repetir falhas com backoff exponencial registrado de 1m, 5m, 30m, 2h e 12h. A reunião também diz cinco tentativas: a contagem exata precisa ser resolvida antes de implementar. Após esgotamento, guardar payload/motivo/data em dead letter separada.
7. Permitir POST /admin/webhooks/dead-letter/:id/replay somente para ADMIN, reinserindo pending e auditando identidade.
8. Oferecer GET /webhooks/:id/deliveries com últimas 100 entregas, sucesso/falha, payload, resposta e tempo.
9. Limitar payload a 64 KB, rejeitando excedente sem truncar. Rotação mantém segredo anterior válido por 24 horas; contrato de assinatura em transição permanece pendente.

## Fora de escopo
- Webhooks de entrada: somente outbound.
- Fallback por e-mail: excluído na reunião.
- Dashboard/UI: outra equipe, fora desta entrega.
- Arquivamento após aproximadamente 30 dias: ideia futura, sem implementação inicial.
- Múltiplos workers/particionamento e ordenação global: expansão futura.
- Implementação de runtime: este desafio entrega documentos, não o módulo de webhooks.

## Requisitos não funcionais
Atomicidade SQL; tolerância a indisponibilidade do receptor; observabilidade via Pino; segredos por endpoint; HTTPS; payload máximo; timeout explícito; auditabilidade de replay. Aproveitar controller/service/repository/routes/schema, Zod, AppError e Prisma existentes. Códigos específicos começam com WEBHOOK_. Latência sob falha/retry pode exceder o objetivo normal de 10 segundos; não prometer exactly once.

## Decisões e dependências
[Outbox MySQL](adrs/ADR-001-outbox-mysql.md), [retry/DLQ](adrs/ADR-002-retry-dead-letter.md), [HMAC](adrs/ADR-003-hmac-endpoint.md), [at least once](adrs/ADR-004-at-least-once.md), [worker](adrs/ADR-005-worker-polling.md) e [padrões](adrs/ADR-006-padroes-existentes.md).
Dependências: MySQL já utilizado, processo separado, cadastro do cliente e validação do receptor. Marcos documentará a integração e a garantia at least once no portal de desenvolvedores, conforme compromisso da reunião [09:26]/[09:40]. Segurança reserva dois dias úteis antes do deploy; proposta de planejamento de três sprints depende de revisão dos design docs antes de codificação.

## Riscos e mitigação
Contradição de tentativas, bloqueio de ordenação durante retry, formato durante rotação, autorização por cliente, retenção de entregas/payloads, taxa de saída e destino HTTPS controlado pelo cliente. A reunião não resolve todos esses pontos; [RFC](RFC.md) explicita responsáveis e impacto. Segredos não devem aparecer em logs; conteúdo armazenado e respostas precisam de política de acesso/retenção antes de produção.

As classificações abaixo são avaliação qualitativa desta revisão, derivadas das falhas debatidas; não probabilidades medidas nem decisões atribuídas à reunião.

| Risco | Probabilidade estimada | Impacto | Mitigação |
|---|---|---|---|
| Receptor indisponível por manutenção ([09:16]) | Média | Alto: atraso/perda sem recuperação | Backoff, DLQ e replay auditado |
| Duplicata após falha de confirmação ([09:24–25]) | Média | Alto: consumidor processa duas vezes | At least once explícito e deduplicação por UUID |
| Vazamento de segredo em cliente ([09:22]) | Média | Alto: falsificação no endpoint comprometido | Segredo por endpoint, rotação 24h e revisão de Segurança |

## Critérios de aceite
- AC01: commit de changeStatus e evento é atômico; rollback não deixa evento órfão.
- AC02: somente clientes/status elegíveis recebem snapshot com campos definidos no FDD, sem itens.
- AC03: receptor deduplica UUID; timeout e falhas seguem política ratificada de retry e dead letter preserva motivo/payload/data.
- AC04: requests HTTPS têm cinco cabeçalhos definidos, assinatura verificável e payload respeita 64 KB.
- AC05: CRUD exige autenticação; replay exige ADMIN e gera registro de auditoria; customer_id não é inferido do JWT.
- AC06: consulta retorna no máximo as últimas 100 entregas com resultado, payload, resposta e tempo.
- AC07: worker roda separado e polling é 2s; ordenação por pedido é testada inclusive com falhas após definição da política.
- AC08: rotação aceita o período de 24h conforme contrato ratificado; assinatura fora da janela é rejeitada pelo verificador de referência.

## Estratégia de testes
Unidade: filtros de status, tamanho em bytes, HMAC, calendário de retry e autorização. Integração MySQL: transação rollback/commit, claim do worker, persistência das tentativas e dead letter, replay. Contrato HTTP: payload/headers e classificação de respostas ratificada. Resiliência: crash após envio e antes de persistir, receptor indisponível, pedido com evento anterior em retry. Segurança: ausência de segredo em logs, roles, validação HTTPS e rotação. Estes são testes planejados para a implementação futura; a validação executada nesta entrega é documental.
