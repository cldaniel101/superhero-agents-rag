from google.adk.agents import Agent
from app.tools.doc_tar_utils import fetch_doc_tar_content
# Prompt do sub‑agente SPIDERMAN
from .prompt import SPIDERMAN_PROMPT


spiderman = Agent(
name="spiderman",
model="gemini-2.0-flash", # foco em raciocínio e extração de conhecimento
description=(
    "Sub-agente que interpreta fielmente o Homem-Aranha (Peter Parker), "
    "trazendo respostas inteligentes, carismáticas e cheias de personalidade. "
    "Ele conversa com fãs diretamente do universo Marvel, mantendo sempre o "
    "Você deverá Ler o conteúdo da TAR-xxxx ou DOC-xxxx e entender se uma missão é para você"
    "tom jovem, espirituoso e heróico do amigão da vizinhança."
),
instruction=SPIDERMAN_PROMPT,
tools=[fetch_doc_tar_content]
)

