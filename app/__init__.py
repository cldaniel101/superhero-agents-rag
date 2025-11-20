"""
Agente de Super-Heróis com RAG

Um pacote para interagir com capacidades RAG do Vertex AI no contexto de super-heróis.
"""

import os

import vertexai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter configuração do Vertex AI do ambiente
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")

# Inicializar Vertex AI no carregamento do pacote
try:
    if PROJECT_ID and LOCATION:
        print(f"Inicializando Vertex AI com project={PROJECT_ID}, location={LOCATION}")
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print("Inicialização do Vertex AI bem-sucedida")
    else:
        print(
            f"Configuração do Vertex AI ausente. PROJECT_ID={PROJECT_ID}, LOCATION={LOCATION}. "
            f"Ferramentas que requerem Vertex AI podem não funcionar corretamente."
        )
except Exception as e:
    print(f"Falha ao inicializar Vertex AI: {str(e)}")
    print("Por favor, verifique suas credenciais do Google Cloud e configurações do projeto.")

# Importar agente após a inicialização estar completa
from .agent import root_agent

