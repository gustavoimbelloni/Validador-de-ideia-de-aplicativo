import os
import json
from typing import Iterator, Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.storage.sqlite import SqliteStorage
from agno.tools.googlesearch import GoogleSearchTools 
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.workflow import Workflow, RunEvent, RunResponse
from httpx import Response
from pydantic import BaseModel, Field
from rich.prompt import Prompt 

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

class AppCoreConcept(BaseModel):
    """Defina o conceito central da ideia do aplicativo"""
    user_problem: str = Field(..., description="O problema que o aplicativo resolve.")
    innovation: str = Field(..., description="Aspecto inovador do aplicativo.")
    feasibility: str = Field(..., description="Viabilidade técnica e operacional do aplicativo.")

class AppMarketAnalysis(BaseModel):
    """Realiza análise de mercado para a ideia do aplicativo"""
    total_addressable_market: str = Field(..., description="Tamanho total do mercado alcançável em unidades monetárias.")
    user_segment: str = Field(..., description="Segmento de usuários alvo do aplicativo.")
    market_trends: str = Field(..., description="Tendências de mercado relevantes para o aplicativo.")

class AppCompetitorReview(BaseModel):
    """Revisa concorrentes diretos do aplicativo"""
    competitors: str = Field(..., description="Descrição dos principais concorrentes do aplicativo.")
    competitive_advantage: str = Field(..., description="Vantagens competitivas do aplicativo em relação aos concorrentes.")
    SWOT_analysis: str = Field(..., description="Análise SWOT do concorrente.")

class AppIdeaValidator(Workflow):
    """Valida a ideia do aplicativo e gera um relatório."""
    #Analisa o conceito central da ideia do aplicativo
    core_concept_agent: Agent = Agent(
        model=OpenAIChat(id="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key),
        instructions=["Analise a ideia do aplicativo e esclareça o conceito principal.", "Identifique o problema principal, os recursos inovadores e a viabilidade técnica e operacional do aplicativo."],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        response_model=AppCoreConcept, debug_mode=False)

    #Analisa o mercado alvo do aplicativo
    market_analysis_agent: Agent = Agent(
        model=OpenAIChat(id="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key),
        tools=[GoogleSearchTools()],
        instructions=["Realize pesquisas de mercado, estime o TAM, identifique segmentos de usuários e analise tendências."],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        response_model=AppMarketAnalysis)

    #Identifica concorrentes e revisa sua análise SWOT
    competitor_review_agent: Agent = Agent(
        model=OpenAIChat(id="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key),
        tools=[GoogleSearchTools()],
        instructions=["Identifique concorrentes diretos, analise suas forças, fraquezas, oportunidades e ameaças (SWOT)."],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        markdown=True, debug_mode=False)

    #Gera o relatório final
    report_agent: Agent = Agent(
        model=OpenAIChat(id="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key),
        instructions=["Gere um relatório detalhado com as análises realizadas, incluindo o TAM, segmentos de usuários, concorrentes, vantagens competitivas e recomendações."],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        markdown=True, debug_mode=False)

    
    def get_core_concept(self, app_idea: str) -> Optional[AppCoreConcept]:
        """Obtém o conceito central da ideia do aplicativo"""
        try:
            response: RunResponse = self.core_concept_agent.run(app_idea)
            if not response or not response.content:
                logger.warning("Não foi possível obter o conceito central da ideia do aplicativo")
            if not isinstance(response.content, AppCoreConcept):
                logger.warning("Tipo de resposta inválido")
            return response.content
        except Exception as e:
            logger.warning(f"Erro ao obter o conceito central da ideia do aplicativo: {str(e)}")
            return None

    def get_market_analysis(self, app_idea: str, core_concept: AppCoreConcept) -> Optional[AppMarketAnalysis]:
        """Obtém a análise de mercado da ideia do aplicativo"""
        agent_input = {"app_idea": app_idea, **core_concept.model_dump()}
        try:
            response: RunResponse = self.market_analysis_agent.run(json.dumps(agent_input, indent=4))
            if not response or not response.content:
                logger.warning("Não foi possível obter a análise de mercado da ideia do aplicativo")
            if not isinstance(response.content, AppMarketAnalysis):
                logger.warning("Tipo de resposta inválido")
            return response.content
        except Exception as e:
            logger.warning(f"Erro ao obter a análise de mercado da ideia do aplicativo: {str(e)}")
        return None

    