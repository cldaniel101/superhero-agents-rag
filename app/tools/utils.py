"""
Funções utilitárias para as ferramentas RAG.
"""

import logging
import re
from typing import Optional

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..config import (
    LOCATION,
    PROJECT_ID,
)

logger = logging.getLogger(__name__)


def obter_nome_recurso_corpus(nome_corpus: str) -> str:
    """
    Converte um nome de corpus para seu nome de recurso completo, se necessário.
    Lida com vários formatos de entrada e garante que o nome retornado siga os requisitos do Vertex AI.

    Args:
        nome_corpus (str): O nome ou nome de exibição do corpus

    Returns:
        str: O nome de recurso completo do corpus
    """
    logger.info(f"Obtendo nome de recurso para corpus: {nome_corpus}")

    # Se já é um nome de recurso completo com o formato projects/locations/ragCorpora
    if re.match(r"^projects/[^/]+/locations/[^/]+/ragCorpora/[^/]+$", nome_corpus):
        return nome_corpus

    # Verifica se é um nome de exibição de um corpus existente
    try:
        # Lista todos os corpora e verifica se há correspondência com o nome de exibição
        corpora = rag.list_corpora()
        for corpus in corpora:
            if hasattr(corpus, "display_name") and corpus.display_name == nome_corpus:
                return corpus.name
    except Exception as e:
        logger.warning(f"Erro ao verificar nome de exibição do corpus: {str(e)}")
        # Se não puder verificar, continua com o comportamento padrão
        pass

    # Se contém elementos de caminho parciais, extrai apenas o ID do corpus
    if "/" in nome_corpus:
        # Extrai a última parte do caminho como ID do corpus
        corpus_id = nome_corpus.split("/")[-1]
    else:
        corpus_id = nome_corpus

    # Remove caracteres especiais que possam causar problemas
    corpus_id = re.sub(r"[^a-zA-Z0-9_-]", "_", corpus_id)

    # Constrói o nome de recurso padronizado
    return f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{corpus_id}"


def verificar_corpus_existe(nome_corpus: str, contexto_ferramenta: Optional[ToolContext] = None) -> bool:
    """
    Verifica se um corpus com o nome fornecido existe.

    Args:
        nome_corpus (str): O nome do corpus a verificar
        contexto_ferramenta (ToolContext): O contexto da ferramenta para gerenciamento de estado

    Returns:
        bool: True se o corpus existe, False caso contrário
    """
    # Verifica o estado primeiro se contexto_ferramenta for fornecido
    if contexto_ferramenta and contexto_ferramenta.state.get(f"corpus_existe_{nome_corpus}"):
        return True

    try:
        # Obtém o nome de recurso completo
        nome_recurso_corpus = obter_nome_recurso_corpus(nome_corpus)

        # Lista todos os corpora e verifica se este existe
        corpora = rag.list_corpora()
        for corpus in corpora:
            if (
                corpus.name == nome_recurso_corpus
                or corpus.display_name == nome_corpus
            ):
                # Atualiza o estado se contexto_ferramenta for fornecido
                if contexto_ferramenta:
                    contexto_ferramenta.state[f"corpus_existe_{nome_corpus}"] = True
                    # Também define este como o corpus atual se nenhum corpus atual estiver definido
                    if not contexto_ferramenta.state.get("corpus_atual"):
                        contexto_ferramenta.state["corpus_atual"] = nome_corpus
                return True

        return False
    except Exception as e:
        logger.error(f"Erro ao verificar se corpus existe: {str(e)}")
        # Se não puder verificar, assume que não existe
        return False


def definir_corpus_atual(nome_corpus: str, contexto_ferramenta: Optional[ToolContext] = None) -> bool:
    """
    Define o corpus atual no estado do contexto da ferramenta.

    Args:
        nome_corpus (str): O nome do corpus a definir como atual
        contexto_ferramenta (ToolContext): O contexto da ferramenta para gerenciamento de estado

    Returns:
        bool: True se o corpus existe e foi definido como atual, False caso contrário
    """
    # Verifica se o corpus existe primeiro
    if contexto_ferramenta and verificar_corpus_existe(nome_corpus, contexto_ferramenta):
        contexto_ferramenta.state["corpus_atual"] = nome_corpus
        return True
    return False

