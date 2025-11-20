from google.adk.agents import Agent
from app.tools.doc_tar_utils import fetch_doc_tar_content
from app.tools import (
    consultar_corpus_rag,
    listar_corpora,
    criar_corpus,
    adicionar_dados,
    obter_info_corpus,
)
# Prompt do sub‑agente SPIDERMAN
from .prompt import SPIDERMAN_PROMPT


spiderman = Agent(
name="spiderman",
model="gemini-2.0-flash", # foco em raciocínio e extração de conhecimento
description=(
    "Sub-agente que interpreta fielmente o Homem-Aranha (Peter Parker), "
    "trazendo respostas inteligentes, carismáticas e cheias de personalidade. "
    "Ele conversa com fãs diretamente do universo Marvel, mantendo sempre o "
    "tom jovem, espirituoso e heróico do amigão da vizinhança. "
    "Pode consultar conhecimento sobre super-heróis através de ferramentas RAG."
),
instruction=SPIDERMAN_PROMPT,
tools=[
    fetch_doc_tar_content,
    consultar_corpus_rag,
    listar_corpora,
    criar_corpus,
    adicionar_dados,
    obter_info_corpus,
]
)

