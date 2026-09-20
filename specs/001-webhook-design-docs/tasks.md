# Tasks: Design Docs de Webhooks

## Phase 1 — Setup
- [x] T001 Inicializar Spec Kit e governança em .specify/memory/constitution.md.
- [x] T002 Especificar entrega e plano em specs/001-webhook-design-docs/spec.md e plan.md.

## Phase 2 — Foundation
- [x] T003 Conferir TRANSCRICAO.md e registrar ambiguidades em specs/001-webhook-design-docs/research.md.
- [x] T004 Fixar inventário rastreável em docs/TRACKER.md.

## Phase 3 — US1: produto e arquitetura
Teste independente: leitor identifica escopo, decisões e pendências sem consultar implementação futura.
- [x] T005 [P] [US1] Redigir requisitos e aceite em docs/PRD.md.
- [x] T006 [P] [US1] Redigir proposta e alternativas em docs/RFC.md.
- [x] T007 [US1] Registrar seis decisões em docs/adrs/ADR-001-outbox-mysql.md até ADR-006-padroes-existentes.md.

## Phase 4 — US2: guia de implementação
Teste independente: contratos, fluxos e caminhos reais permitem planejar desenvolvimento, mantendo decisões pendentes visíveis.
- [x] T008 [US2] Detalhar transação, worker, HTTP, erros e testes em docs/FDD.md.

## Phase 5 — US3: auditoria
Teste independente: fontes/localizações conferíveis, links válidos e base intacta.
- [x] T009 [US3] Reconciliar cobertura e origem em docs/TRACKER.md.
- [x] T010 [P] [US3] Documentar prompts reais e iterações em README.md.
- [x] T011 [US3] Validar documentos e base com scripts/validate_docs.py.

## Phase 6 — Polish
- [x] T012 Revisar consistência e registrar resultado em specs/001-webhook-design-docs/validation.md.
- [x] T013 Executar convergência e revisar diff antes do commit; registrar em specs/001-webhook-design-docs/convergence.md.

## Dependencies and parallelism
T001→T002→T003→T004. US1: T005 e T006 podem ser redigidas em paralelo; T007 consolida decisões. US2 sucede US1. US3: README pode ser redigido enquanto tracker é conferido; validação depende de todos. US2 é uma tarefa única, sem paralelismo artificial. MVP documental: US1; entrega completa exige US2/US3 e polish.

## Phase 7 — Correção da revisão independente
- [x] T014 [US2] Corrigir assinatura de AppError em docs/FDD.md conforme src/shared/errors/app-error.ts: message é argumento obrigatório antes de statusCode/errorCode; details é opcional.
