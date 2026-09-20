# Design Docs de Webhooks Constitution

## Core Principles

### I. Rastreabilidade obrigatória
Todo requisito ou decisão DEVE apontar para TRANSCRICAO.md ou código real. O tracker cobre ao menos 80% dos itens; decisões não fechadas permanecem explicitamente abertas.

### II. Preservação da base
TRANSCRICAO.md, src/, prisma/ e tests/ DEVEM permanecer byte a byte iguais à base. Esta entrega produz documentos; não implementa a feature de webhooks.

### III. Separação dos documentos
PRD descreve produto; RFC propõe arquitetura; ADR registra decisão; FDD detalha implementação; TRACKER liga conteúdo às fontes. Duplicação de escopo DEVE ser revisada.

### IV. Validação verificável
Caminhos, timestamps, links, cobertura do tracker e integridade da base DEVEM ser verificados antes do commit. Nenhum resultado de execução pode ser inventado.

### V. Escopo mínimo e decisões honestas
As decisões fechadas na reunião prevalecem. Ambiguidades sobre contagem de retries, ordering sob falha e rotação de secrets DEVEM ficar explícitas, sem atribuir uma solução inventada aos participantes.

## Restrições da entrega
Entregar docs/PRD.md, RFC.md, FDD.md, TRACKER.md, cinco a oito ADRs e README com processo. Documentos em PT-BR. Não incluir chaves, credenciais ou transcrições de aulas privadas. A transcrição da reunião fornecida no starter é a fonte pública do desafio.

## Workflow e critérios de revisão
Spec Kit: constitution, specify, plan, tasks, implement e converge, em etapas separadas. Revisar cada resultado antes de avançar. Commits apenas após validação e inspeção do diff. Branch feature/sdd-fase-299; envio na plataforma fica para etapa posterior.

## Governance
Versão inicial 1.0.0 adotada em 2026-09-19 para esta entrega. Alterações exigem justificativa e nova versão: major para quebra de princípio, minor para adição, patch para esclarecimento. Toda revisão deve conferir estes cinco princípios.

**Version**: 1.0.0 | **Ratified**: 2026-09-19 | **Last Amended**: 2026-09-19
