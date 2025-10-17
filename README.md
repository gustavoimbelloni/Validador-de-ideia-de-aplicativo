## Google-Calendario-Agno

Integração simples com Google Calendar usando Agno (Agent + Tools) e OpenRouter. O agente entende comandos em português e lista/cria eventos no seu calendário Google após autenticação OAuth.

### Recursos
- Assistente em PT-BR com instruções contextuais (data/hora e fuso)
- Leitura de eventos do Google Calendar
- Criação de eventos/tarefas (escopo de escrita habilitado)
- OAuth 2.0 com armazenamento de `token.json` local (não versionado)

### Arquitetura rápida
- `calendar_integration.py`: cria um `Agent` do Agno com o modelo `OpenAIChat` (via OpenRouter) e a ferramenta `GoogleCalendarTools`.
- `GoogleCalendarTools`: faz a autenticação e chama a API do Google Calendar.

---

## Pré-requisitos
- Python 3.12+
- Conta Google com Google Calendar habilitado
- Projeto no Google Cloud com OAuth consent configurado
- Chave de API do OpenRouter (`OPENROUTER_API_KEY`)

### Dependências (pip)
Instale em um virtualenv:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirement.txt
```

Alternativa (pyproject com uv):
```powershell
uv venv
uv sync
```

---

## Segredos e credenciais
Este projeto não versiona segredos. Já há regras no `.gitignore` para ignorar `.env`, `token.json`, `client_secret*.json`, `.secrets/` e `.venv/`.

Você tem duas formas de fornecer as credenciais do Google OAuth:

1) Arquivo JSON (recomendado para iniciantes)
- Crie a pasta `.secrets/` na raiz do projeto
- Salve o arquivo do cliente OAuth do Google como `.secrets/client_secret.json`
  - Tipo do cliente: "Aplicativo para computador" (Desktop)
  - Ative a Google Calendar API no projeto
- O código já aponta por padrão para `.secrets/client_secret.json`

2) Variáveis de ambiente
- Defina `GOOGLE_CREDENTIALS_PATH` apontando para o caminho do JSON
- Alternativamente, informe os campos via env (se não usar arquivo):
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_PROJECT_ID`, `GOOGLE_REDIRECT_URI`

Exemplo de `.env` (não versionar):
```env
# OpenRouter
OPENROUTER_API_KEY=sk-or-v1_xxxxxxxxxxxxxxxxxxxxxxxxx

# Opção A: Usar arquivo JSON
GOOGLE_CREDENTIALS_PATH=C:\\Users\\SEU_USUARIO\\Desktop\\Curso_agno\\.secrets\\client_secret.json

# Opção B: Sem arquivo (client config via env)
# GOOGLE_CLIENT_ID=...
# GOOGLE_CLIENT_SECRET=...
# GOOGLE_PROJECT_ID=...
# GOOGLE_REDIRECT_URI=http://localhost:8765
```

---

## Execução
1) Ative o virtualenv
```powershell
.\.venv\Scripts\activate
```
2) Execute o script
```powershell
python calendar_integration.py
```
3) Na primeira execução, será aberto o fluxo OAuth no navegador
- Selecione a conta certa e conceda as permissões
- O arquivo `token.json` será criado e reutilizado nas próximas execuções

> Observação: o script usa a porta `8765` para o callback OAuth. Se estiver ocupada, ajuste em `calendar_integration.py` no parâmetro `oauth_port` da ferramenta.

---

## O que o script faz
- Imprime a lista de eventos de hoje
- Cria uma "tarefa" (evento) às 22:00 do dia atual (padrão)

Você pode personalizar no arquivo `calendar_integration.py`:
- Texto das instruções (em PT-BR)
- Horário e fuso do evento
- Permissões (coloque `allow_update=False` para somente leitura)

---

## Publicação no GitHub
Para subir apenas o arquivo principal e `.gitignore`:
```powershell
git init
git add calendar_integration.py .gitignore
git commit -m "feat: integração Google Calendar com Agno (sem segredos)"
git branch -M master
git remote add origin https://github.com/SEU_USUARIO/Google-Calendario-Agno.git
git push -u origin master
```

> Garanta que nenhum segredo foi adicionado ao commit. Nunca versione `.env`, `token.json` ou o `client_secret.json`.

---

## Solução de problemas
- 403 access_denied no OAuth:
  - Adicione seu e-mail como "Usuário de teste" na tela de consentimento
  - Confirme que o cliente é do tipo "Aplicativo para computador" ou que o `redirect_uri` está autorizado
- Porta ocupada (WinError 10048):
  - Troque `oauth_port` (ex.: 8766) e rode de novo
- "Google client libraries not found":
  - `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
- Trocar escopo (apenas leitura):
  - Ajuste `allow_update=False` na criação do `GoogleCalendarTools`
- Renovar consentimento:
  - Apague `token.json` e rode novamente para refazer o login

---


## Aviso de segurança
Se credenciais forem expostas acidentalmente:
1) Revogue/rote a credencial no Google Cloud
2) Remova do índice e do histórico Git
   - `git rm --cached client_secret*.json && git commit && git push`
   - `pip install git-filter-repo && git filter-repo --invert-paths --path-glob "client_secret*.json" && git push --force`

---

## Licença
Livre para uso educacional e demonstrações.


