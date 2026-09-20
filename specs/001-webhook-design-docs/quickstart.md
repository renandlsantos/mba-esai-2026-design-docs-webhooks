# Verificação da entrega

1. Leia README.md e navegue PRD → RFC → ADRs → FDD → TRACKER.
2. Execute `python3 scripts/validate_docs.py` na raiz do repositório.
3. Execute `git diff --exit-code upstream/main -- TRANSCRICAO.md src prisma tests` para conferir a preservação da base (caso a referência upstream tenha avançado, compare com o commit-base registrado no relatório de validação).
4. Leia os pontos abertos do RFC: não representam implementação concluída ou decisões ratificadas.
5. Antes de commit: `git diff --check` e revisão dos arquivos adicionados, sem segredos ou acervo privado.

Não é necessário instalar Node, iniciar MySQL ou fornecer credenciais para validar documentos.
