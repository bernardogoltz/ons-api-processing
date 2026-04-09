# Estrutura do Projeto com uv

## O que é o uv

[uv](https://docs.astral.sh/uv/) é um gerenciador de pacotes e ambientes virtuais Python, escrito em Rust. Ele substitui `pip`, `pip-tools`, `virtualenv` e `pyenv` em uma única ferramenta. É ordens de grandeza mais rápido que pip.

## Arquivos do projeto

| Arquivo | O que faz |
|---|---|
| `pyproject.toml` | Metadados do projeto, dependências e configurações de build |
| `uv.lock` | Lock file com versões exatas de todas as dependências (equivalente ao `requirements.txt` pinado) |
| `.python-version` | Versão do Python usada no projeto (`3.12`) |
| `.venv/` | Ambiente virtual criado automaticamente pelo uv |

## Como inicializar um projeto do zero

```bash
# Criar um novo projeto
uv init meu-projeto
cd meu-projeto

# Isso gera:
#   pyproject.toml    — configuração do projeto
#   .python-version   — versão do Python
#   hello.py          — arquivo de exemplo
```

Para projetos com estrutura `src/`:

```bash
uv init --lib meu-pacote
# Gera src/meu_pacote/__init__.py e pyproject.toml com build system
```

## Ambiente virtual (.venv)

O uv cria e gerencia o `.venv/` automaticamente. Você **não precisa** ativar o ambiente manualmente.

```bash
# Cria .venv/ e instala tudo que está no pyproject.toml + uv.lock
uv sync
```

O que `uv sync` faz:

1. Lê `pyproject.toml` para saber as dependências
2. Resolve versões usando `uv.lock` (ou cria o lock se não existir)
3. Cria `.venv/` no diretório do projeto (se não existir)
4. Instala o Python da versão em `.python-version` (se necessário)
5. Instala todas as dependências no `.venv/`
6. Instala o próprio pacote em modo editável

Após `uv sync`, a pasta `.venv/` contém o interpretador Python e todos os pacotes. O uv sabe encontrá-la automaticamente — sem necessidade de `source .venv/bin/activate`.

## Comandos do dia a dia

```bash
# Rodar qualquer script ou comando dentro do ambiente
uv run python meu_script.py
uv run pytest
uv run ons-carga SE 2024-01-15

# Adicionar uma dependência nova
uv add requests
uv add "pandas>=2.0"

# Adicionar dependência de desenvolvimento
uv add --dev pytest ruff

# Remover uma dependência
uv remove httpx

# Atualizar dependências para últimas versões compatíveis
uv lock --upgrade
uv sync
```

## uv run vs python direto

`python` usa o interpretador padrão do sistema (ou do conda, se ativo). `uv run` sempre usa o `.venv` do projeto:

```
> uv run python -c "import sys; print(sys.executable)"
C:\...\ONS_API_processing\.venv\Scripts\python.exe    # ← .venv do projeto

> python -c "import sys; print(sys.executable)"
C:\...\anaconda3\python.exe                            # ← conda base
```

Com `uv run`, não importa qual ambiente conda/sistema está ativo — ele sempre resolve o `.venv` local. Sem necessidade de `conda deactivate` ou `activate`.

Se preferir ativar o `.venv` manualmente:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

## uv.lock

O `uv.lock` é gerado automaticamente e garante builds reproduzíveis. Ele trava as versões exatas de **todas** as dependências (diretas e transitivas). Deve ser commitado no git.

```bash
# Regenerar o lock a partir do pyproject.toml
uv lock

# Atualizar tudo para últimas versões
uv lock --upgrade

# Atualizar apenas um pacote
uv lock --upgrade-package pandas
```

## Resumo

| Ação | Comando |
|---|---|
| Criar projeto | `uv init` |
| Instalar tudo | `uv sync` |
| Rodar comando | `uv run <comando>` |
| Adicionar pacote | `uv add <pacote>` |
| Remover pacote | `uv remove <pacote>` |
| Atualizar lock | `uv lock --upgrade` |
| Ver versão do uv | `uv --version` |
