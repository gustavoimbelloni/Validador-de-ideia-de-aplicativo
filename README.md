## 💡 Validador de Ideias de App

Valide rapidamente uma ideia de aplicativo (conceito, mercado, concorrentes) e gere um relatório em Markdown usando modelos via OpenRouter. Disponível em CLI e interface web com Streamlit.

### 📦 Tecnologias
- `agno` (agentes, workflows e ferramentas)
- `OpenRouter` (acesso a modelos LLM)
- `pydantic`, `rich`
- `streamlit` (UI opcional)

---

## ✅ Pré-requisitos
- Python 3.10+
- Uma chave de API do OpenRouter

Crie sua conta e uma API key em `https://openrouter.ai`.

---

## ⚙️ Instalação

### Windows (PowerShell)
```powershell
# Na pasta do projeto
py -m venv .venv
. .\.venv\Scripts\Activate.ps1

pip install -U pip
pip install -r requirements.txt

# Arquivo de ambiente (.env na pasta do projeto)
New-Item -ItemType File -Path .env -Force | Out-Null
Add-Content .env "OPENROUTER_API_KEY=xxxx"
# (Edite o valor com sua chave real)
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt

# Crie o arquivo .env
printf "OPENROUTER_API_KEY=xxxx\n" > .env
# (Edite o valor com sua chave real)
```

---

## 🚀 Uso

### CLI
```bash
python validating_ideas.py
```
Siga o prompt e informe sua ideia. Um relatório em Markdown será exibido no terminal.

### Interface Web (Streamlit)
```bash
streamlit run streamlit_app.py
```
Abra o link local exibido no terminal. Preencha a ideia, gere o relatório e (opcionalmente) faça o download como `.md`.

---

## 🔐 Variáveis de Ambiente
Arquivo `.env`:
```env
OPENROUTER_API_KEY=xxxx
```

---

## 🗂️ Estrutura do Projeto
```text
new_project/
├─ validating_ideas.py        # Fluxo principal (CLI) e agentes
├─ streamlit_app.py           # UI web com Streamlit
├─ requirements.txt           # Dependências
├─ (crie) .env                # Variáveis de ambiente locais
├─ tmp/
│  └─ agno_workflow.db        # Estado/armazenamento do workflow
└─ README.md
```

---

## ℹ️ Notas
- O pacote `agno` fornece `Agent`, `Workflow`, `SqliteStorage` e utilitários.
- O modelo é acessado via OpenRouter com `OpenAIChat` e `base_url` do OpenRouter.
- O `GoogleSearchTools` é utilizado nas etapas de mercado e concorrentes.

---

## 🧰 Solução de Problemas
- "OPENROUTER_API_KEY não encontrada": verifique se o `.env` existe e contém a chave.
- Erros de rede/timeout: tente novamente e confira sua conexão.
- Ambiente virtual: garanta que o venv esteja ativo ao instalar/rodar.

---

## 📄 Licença
Este projeto é distribuído sob a licença MIT.