# Design Docs de Webhooks — MBA Engenharia de Software com IA

## Sobre o desafio
Esta entrega transforma a reunião do starter e a leitura da aplicação de pedidos em um pacote de documentos para uma feature de webhooks outbound. O objetivo é explicar produto, arquitetura, decisões e integração com o código, com rastreabilidade suficiente para revisão antes de implementar.

O código da aplicação, o schema, os testes e a transcrição permanecem intactos. Este repositório não implementa webhooks nem demonstra uma API de webhooks funcionando. É um fork do [starter oficial](https://github.com/devfullcycle/mba-ia-desafio-design-docs-com-ia); o enunciado original está no histórico do README, commit `e7f6311b96ee3b21bf8cb7077f53a6e4045143eb`.

## Ferramentas de IA utilizadas
- Codex: leitura dirigida da transcrição/código, elaboração e revisão dos documentos e construção da validação documental.
- [GitHub Spec Kit](https://github.com/github/spec-kit), specify-cli 1.0.8, integração Codex: constituição → especificação → plano → tarefas → implementação documental → convergência. Os artefatos estão em [.specify/memory/constitution.md](.specify/memory/constitution.md) e [specs/001-webhook-design-docs](specs/001-webhook-design-docs/spec.md).
- Python 3 (biblioteca padrão) e Git: checks reproduzíveis de estrutura, links, fontes, exemplos JSON e preservação da base. Não são ferramentas de geração de conteúdo.

## Workflow adotado
1. Ler enunciado, TRANSCRICAO.md e integrações reais: OrderService.changeStatus, auth, middleware de erros, router e Prisma.
2. Fixar escopo documental na constituição/especificação; revisar checklist antes do plano e das 13 tarefas.
3. Produzir PRD/RFC iniciais, detalhar FDD, formalizar seis ADRs e construir inventário rastreável. A sequência escolhida foi iterativa; não se alega execução literal da ordem sugerida ADR-first.
4. Confrontar cada contrato com reunião/código, corrigir nomes, completar rotação e separar propostas de decisões.
5. Revisar critérios do enunciado, adicionar riscos estruturados e exemplos HTTP; validar base/links/fontes e registrar convergência.

Foram consultadas as aulas do acervo local sobre PRD (16966, 16967, 16968, 16969) para manter a distinção entre problema/valor/escopo e implementação. Nenhuma transcrição privada ou arquivo do acervo foi copiado para este repositório. A fonte dos requisitos é a transcrição pública fornecida pelo starter, e a fonte dos pontos de integração é seu código.

## Prompts customizados
Os blocos abaixo registram os direcionamentos de trabalho usados nesta sessão, normalizados para leitura; não são uma transcrição literal do chat nem uma alegação de execução por outro modelo.

```text
Leia a transcrição e os caminhos reais do starter. Produza um pacote documental,
sem alterar TRANSCRICAO.md, src, prisma ou tests. Separe PRD (por quê/o quê),
RFC (proposta/alternativas/pontos abertos), FDD (contratos e integração) e seis
ADRs das decisões centrais. Preserve os itens fora de escopo. Quando a fonte
não resolver um detalhe, identifique-o como proposta ou pergunta, não como
requisito aprovado. Registre especialmente cinco tentativas versus cinco
intervalos e ordenação durante retry.
```

```text
Revise os documentos contra os critérios do enunciado e o código. O FDD tem
pelo menos quatro endpoints com request/response/status e quatro caminhos
existentes? O PRD tem riscos com probabilidade, impacto e mitigação? JWT
contém customer_id? Rotação tem endpoint? Monte tracker com timestamp e
falante ou caminho real; confira links e exemplos JSON. Preserve o código-base
e registre correções concretas, sem alegar testes de runtime não executados.
```

## Iterações e ajustes
Três ciclos principais de redação/revisão documental:
1. **Escopo e arquitetura:** a reunião combina cinco tentativas com cinco intervalos. Em vez de escolher silenciosamente uma contagem, Q01 mantém a contradição explícita. A ordenação apenas por created_at não resolve eventos anteriores em retry; Q02 e a proposta de bloqueio por pedido tornam o risco visível.
2. **Conferência com fonte/código:** corrigidos nomes de clientes para MaxDistribuição e Nova Cargo; confirmado Order.orderNumber como string no Prisma; adicionada a rota proposta de rotação, pois a reunião exige rotação via API. customer_id ficou explícito, pois o JWT atual tem operador/role, não cliente.
3. **Critérios e profundidade:** o primeiro FDD tinha tabela de endpoints, mas faltavam exemplos request/response suficientes. Foram acrescentados seis exemplos de operações; o PRD recebeu matriz de probabilidade/impacto/mitigação. O tracker passou a incluir os refinamentos derivados do código, evitando apresentar a cobertura da reunião como se fosse automaticamente cobertura de todos os documentos.

A revisão é assistida por IA. Não se atribui aos participantes fictícios uma aprovação que não aconteceu, nem se simula uma revisão humana do aluno.

## Como navegar a entrega
1. [PRD](docs/PRD.md): problema, público, objetivos, requisitos, fora de escopo, riscos e aceite.
2. [RFC](docs/RFC.md): proposta concisa, alternativas, riscos e questões abertas.
3. ADRs: [outbox](docs/adrs/ADR-001-outbox-mysql.md), [retry/DLQ](docs/adrs/ADR-002-retry-dead-letter.md), [HMAC](docs/adrs/ADR-003-hmac-endpoint.md), [at least once](docs/adrs/ADR-004-at-least-once.md), [worker](docs/adrs/ADR-005-worker-polling.md), [padrões](docs/adrs/ADR-006-padroes-existentes.md).
4. [FDD](docs/FDD.md): transação, worker, contratos, exemplos, erros, observabilidade e testes planejados.
5. [TRACKER](docs/TRACKER.md): 68 grupos mapeados, 53 da transcrição e 15 do código; metodologia e limites explícitos.
6. [Plano](specs/001-webhook-design-docs/plan.md), [tarefas](specs/001-webhook-design-docs/tasks.md) e [validação](specs/001-webhook-design-docs/validation.md).

## Validação reproduzível
Em um clone com Python 3 e Git:
```sh
python3 scripts/validate_docs.py
git diff --check
```
O validador verifica integridade da base em relação ao commit original, estrutura mínima, seis ADRs, links locais, fontes/timestamps, proporção do tracker e JSON dos exemplos. Não comprova sozinho a qualidade semântica ou cobertura de cada frase: a revisão manual continua necessária. Não requer instalação de dependências da aplicação, MySQL, LLM ou chave de API.

Pontos abertos do RFC são questões do desenho a decidir antes da implementação futura; não são funcionalidades faltantes de uma implementação prometida por esta entrega. Nenhuma submissão na plataforma foi realizada.
