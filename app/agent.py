from google.adk.agents import Agent
from .prompt import ROOT_AGENT_PROMPT
from .sub_agents.captain_america.agent import captain_america
from .sub_agents.spiderman.agent import spiderman
from .sub_agents.frodo.agent import frodo
from .tools.doc_tar_utils import fetch_doc_tar_content
from .tools import (
    consultar_corpus_rag,
    listar_corpora,
    criar_corpus,
    adicionar_dados,
    obter_info_corpus,
)


root_agent = Agent(
    name="especialista",
    model="gemini-2.0-flash",
    description=(
        "Agente orquestrador responsável por introduzir o universo dos super-heróis "
        "e conduzir o usuário a uma conversa pessoal com seu herói favorito. "
        "Interpreta documentos e tarefas e encaminha ao subagente mais qualificado. "
        "Garante uma experiência imersiva, fluida e mágica, conectando fãs a figuras "
        "lendárias como Homem-Aranha, Frodo Bolseiro e Capitão América, "
        "sem revelar a existência de subagentes ou estruturas técnicas.\n\n"
        "1️⃣ Se a mensagem contiver '@nome' (ex.: @spiderman, @frodo, @captain_america), "
        "DELEGUE imediatamente ao subagente correspondente e pare de responder.\n"
        "2️⃣ Se o usuário disser 'quero falar com X' (sem '@'), delegue igualmente.\n"
        "3️⃣ Nunca responda com o conteúdo do subagente; apenas roteie o turno para ele.\n"
        "4️⃣ Sinônimos: @spiderman ~ 'homem aranha'; @captain_america ~ 'capitão américa'.\n\n"
        "Tem acesso a ferramentas RAG para consultar e gerenciar bases de conhecimento sobre super-heróis."
    ),
    instruction=ROOT_AGENT_PROMPT,
    sub_agents=[frodo, spiderman, captain_america],
    tools=[
        fetch_doc_tar_content,
        consultar_corpus_rag,
        listar_corpora,
        criar_corpus,
        adicionar_dados,
        obter_info_corpus,
    ],
)

