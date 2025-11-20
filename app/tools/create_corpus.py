"""
Ferramenta para criar um novo corpus RAG do Vertex AI.
"""

import re
from typing import Optional

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..config import (
    MODELO_EMBEDDING_PADRAO,
)
from .utils import verificar_corpus_existe


def _criar_corpus_impl(
    nome_corpus: str,
    contexto_ferramenta: Optional[ToolContext] = None,
) -> dict:
    """
    Cria um novo corpus RAG do Vertex AI com o nome especificado.

    Args:
        nome_corpus (str): O nome para o novo corpus
        contexto_ferramenta (ToolContext): O contexto da ferramenta para gerenciamento de estado

    Returns:
        dict: Informações de status sobre a operação
    """
    # Verifica se o corpus já existe
    if contexto_ferramenta and verificar_corpus_existe(nome_corpus, contexto_ferramenta):
        return {
            "status": "info",
            "mensagem": f"O corpus '{nome_corpus}' já existe",
            "nome_corpus": nome_corpus,
            "corpus_criado": False,
        }

    try:
        # Limpa o nome do corpus para uso como nome de exibição
        nome_exibicao = re.sub(r"[^a-zA-Z0-9_-]", "_", nome_corpus)

        # Configura o modelo de embedding
        configuracao_modelo_embedding = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model=MODELO_EMBEDDING_PADRAO
            )
        )

        # Cria o corpus
        corpus_rag = rag.create_corpus(
            display_name=nome_exibicao,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=configuracao_modelo_embedding
            ),
        )

        # Atualiza o estado para rastrear a existência do corpus
        if contexto_ferramenta:
            contexto_ferramenta.state[f"corpus_existe_{nome_corpus}"] = True
            # Define este como o corpus atual
            contexto_ferramenta.state["corpus_atual"] = nome_corpus

        return {
            "status": "sucesso",
            "mensagem": f"Corpus '{nome_corpus}' criado com sucesso",
            "nome_corpus": corpus_rag.name,
            "nome_exibicao": corpus_rag.display_name,
            "corpus_criado": True,
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao criar corpus: {str(e)}",
            "nome_corpus": nome_corpus,
            "corpus_criado": False,
        }


def criar_corpus(
    nome_corpus: str,
) -> dict:
    """
    Cria um novo corpus RAG do Vertex AI com o nome especificado.
    Esta é a função pública que o ADK chama, sem o parâmetro ToolContext.

    Args:
        nome_corpus (str): O nome para o novo corpus

    Returns:
        dict: Informações de status sobre a operação
    """
    return _criar_corpus_impl(nome_corpus, None)

