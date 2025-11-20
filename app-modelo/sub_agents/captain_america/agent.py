from google.adk.agents import Agent

# Prompt do sub‑agente CAPTAIN_AMERICA
from .prompt import CAPTAIN_AMERICA_PROMPT



captain_america = Agent(
name="captain_america",
model="gemini-2.0-flash", # foco em raciocínio e extração de conhecimento
description=(
    "Sub-agente que representa o Capitão América (Steve Rogers), oferecendo "
    "respostas firmes, inspiradoras e cheias de valores morais. Ele interage com "
    "fãs mantendo a postura de um verdadeiro herói da nação, com referências à sua "
    "trajetória como líder dos Vingadores e veterano da Segunda Guerra Mundial."
),
instruction=CAPTAIN_AMERICA_PROMPT,
)