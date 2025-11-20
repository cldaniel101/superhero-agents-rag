from google.adk.agents import Agent

# Prompt do sub‑agente FRODO
from .prompt import FRODO_PROMPT
from app.tools.doc_tar_utils import fetch_doc_tar_content


frodo = Agent(
name="frodo",
model="gemini-2.0-flash",
description=(
    "Sub-agente que incorpora Frodo Bolseiro, o hobbit do Condado que carregou "
    "o Um Anel até Mordor. Ele responde de forma serena, sábia e emocional, "
    "compartilhando experiências da Terra-Média com humildade, sempre respeitando "
    "a linguagem, valores e atmosfera do mundo criado por Tolkien."
),
instruction=FRODO_PROMPT,
tools=[fetch_doc_tar_content]
)

