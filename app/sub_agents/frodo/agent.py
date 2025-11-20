from google.adk.agents import Agent
from app.tools.doc_tar_utils import fetch_doc_tar_content
from app.tools import (
    consultar_corpus_rag,
    listar_corpora,
    criar_corpus,
    adicionar_dados,
    obter_info_corpus,
)

# Prompt do sub‑agente FRODO
from .prompt import FRODO_PROMPT


frodo = Agent(
name="frodo",
model="gemini-2.0-flash",
description=(
    "Sub-agente que incorpora Frodo Bolseiro, o hobbit do Condado que carregou "
    "o Um Anel até Mordor. Ele responde de forma serena, sábia e emocional, "
    "compartilhando experiências da Terra-Média com humildade, sempre respeitando "
    "a linguagem, valores e atmosfera do mundo criado por Tolkien. "
    "Pode consultar conhecimento sobre super-heróis através de ferramentas RAG."
),
instruction=FRODO_PROMPT,
tools=[
    fetch_doc_tar_content,
    consultar_corpus_rag,
    listar_corpora,
    criar_corpus,
    adicionar_dados,
    obter_info_corpus,
]
)

