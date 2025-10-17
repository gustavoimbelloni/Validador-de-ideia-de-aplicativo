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
today_at_10pm = now.replace(hour=22, minute=0, second=0, microsecond=0)

event_end = today_at_10pm + datetime.timedelta(hours=1)

agent = Agent(
    model=OpenAIChat(id="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key),
    tools=[GoogleCalendarTools(credentials_path=credentials_path, oauth_port=8765, allow_update=True)],
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
    "summary": "Preencha o relatório do projeto",
    "description": "Trabalhe no relatório do projeto até o final do dia.", 
    "due": {
        "dateTime": today_at_10pm.isoformat(),
        "timeZone": "America/Sao_Paulo",
    }, 
    "status": "needsAction", 
}

agent.print_response(f"Crie uma nova tarefa: {task_details}", markdown=True)