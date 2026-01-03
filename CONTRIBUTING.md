# Contributing

Obrigado por considerar contribuir! Algumas diretrizes rápidas:

- Abra uma issue antes de implementar mudanças grandes.
- Escreva testes para novas funcionalidades e execute `pytest` localmente.
- Siga o estilo PEP8. Sugestões: use `black` e `ruff`.

Formatadores/linters:

- Formate o código com `black` (`python -m black .`) e verifique com `ruff` (`ruff check .`).
- Recomendado: instale e ative `pre-commit` para rodar `black` e `ruff` automaticamente antes de cada commit:

```bash
python -m pip install -U pre-commit
pre-commit install
pre-commit run --all-files
```

- Para adicionar novas bandeiras, atualize `patterns.py` e adicione testes em `tests/`.

Processo de PR:

1. Fork e branch com nome claro
2. Abra um PR apontando para a branch `main` do repositório original
3. Adicione uma das labels apropriadas ao PR para categorizar as mudanças (ex.: `feature`, `bug`, `maintenance`, `documentation`, `tests`) — isso ajuda o release drafter a organizar o changelog automaticamente
4. Espere CI rodar e responda comentários

Rótulos recomendados:

- `feature` — novas funcionalidades
- `bug` — correções de bug
- `maintenance` — mudanças internas / atualizações
- `documentation` — documentação
- `tests` — alterações nos testes

Segurança:

- Para reportar vulnerabilidades, veja `SECURITY.md` no repositório e utilize o recurso de Security Advisories do GitHub ou envie uma mensagem privada para o contato indicado.
