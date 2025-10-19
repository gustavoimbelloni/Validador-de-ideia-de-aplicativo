import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.googlecalendar import GoogleCalendarTools
import datetime
from tzlocal import get_localzone_name

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Caminho do JSON de credenciais do Google (não versionado)
credentials_path = os.getenv(
    "GOOGLE_CREDENTIALS_PATH",
    os.path.join(os.path.dirname(__file__), ".secrets", "client_secret.json"),
)

now = datetime.datetime.now()

# Evento deve começar na hora da execução e durar 1h
event_start = now
event_end = event_start + datetime.timedelta(hours=1)

# Escopos explícitos para evitar erros de invalid_scope
READ_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"
WRITE_SCOPE = "https://www.googleapis.com/auth/calendar"

# Instancia a ferramenta com escopos corretos
calendar_tools = GoogleCalendarTools(
    credentials_path=credentials_path,
    oauth_port=8765,
    allow_update=True,
    scopes=[READ_SCOPE, WRITE_SCOPE],
)

# Workaround: garantir que leitura do token use lista de escopos
# (algumas versões podem usar DEFAULT_SCOPES incorretamente)
try:
    from agno.tools import googlecalendar as _gcal_mod  # type: ignore
    _gcal_mod.GoogleCalendarTools.DEFAULT_SCOPES = [READ_SCOPE, WRITE_SCOPE]  # type: ignore
except Exception:
    pass

agent = Agent(
    model=OpenAIChat(id="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key),
    tools=[calendar_tools],
    show_tool_calls=True,
    instructions=[
        f"""
        Você é um assistente pessoal de tarefas e calendário. Hoje é {datetime.datetime.now()} e o fuso horário do usuário é 
        {get_localzone_name()}. Você ajudará com as seguintes ações no Google Calendar:
        - Consultar eventos agendados em datas e horários específicos.
        - Criar novos eventos com base nos detalhes fornecidos.
        - Adicionar tarefas e gerenciá-las no Google Calendar.
        """
    ],
    add_datetime_to_instructions=True,
)

agent.print_response("Mostre a lista de eventos de hoje", markdown=True)

task_details = {
    "title": "Preencha o relatório do projeto",
    "description": "Trabalhe no relatório do projeto na próxima hora.",
    "start_date": event_start.isoformat(timespec="seconds"),
    "end_date": event_end.isoformat(timespec="seconds"),
    "timezone": get_localzone_name(),
}

agent.print_response(f"Crie um evento com estes detalhes: {task_details}", markdown=True)