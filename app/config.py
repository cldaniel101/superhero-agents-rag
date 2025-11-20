"""
Configurações do Agente RAG para Super-Heróis.

Essas configurações são usadas pelas ferramentas RAG.
A inicialização do Vertex AI é realizada no __init__.py do pacote.
"""

import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Vertex AI
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
RAG_CORPUS = os.environ.get("RAG_CORPUS")

# Configurações RAG
TAMANHO_CHUNK_PADRAO = 512
SOBREPOSICAO_CHUNK_PADRAO = 100
TOP_K_PADRAO = 3
THRESHOLD_DISTANCIA_PADRAO = 0.5
MODELO_EMBEDDING_PADRAO = "publishers/google/models/text-multilingual-embedding-002"
REQUISICOES_EMBEDDING_POR_MIN_PADRAO = 1000

