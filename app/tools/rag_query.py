"""
Ferramenta para consultar corpora RAG do Vertex AI e recuperar informações relevantes.
"""

import logging
from typing import Optional

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..config import (
    THRESHOLD_DISTANCIA_PADRAO,
    TOP_K_PADRAO,
)
from .utils import verificar_corpus_existe, obter_nome_recurso_corpus


def _consultar_corpus_rag_impl(
    nome_corpus: str,
    consulta: str,
    contexto_ferramenta: Optional[ToolContext] = None,
) -> dict:
    """
    Consulta um corpus RAG do Vertex AI com uma pergunta do usuário e retorna informações relevantes.

    Args:
        nome_corpus (str): O nome do corpus a consultar. Se vazio, o corpus atual será usado.
                         Preferencialmente use o resource_name dos resultados de listar_corpora.
        consulta (str): O texto da consulta para buscar no corpus
        contexto_ferramenta (ToolContext): O contexto da ferramenta

    Returns:
        dict: Os resultados da consulta e o status
    """
    try:

        # Verifica se o corpus existe (só verifica se contexto_ferramenta for fornecido)
        if contexto_ferramenta and not verificar_corpus_existe(nome_corpus, contexto_ferramenta):
            return {
                "status": "erro",
                "mensagem": f"O corpus '{nome_corpus}' não existe. Por favor, crie-o primeiro usando a ferramenta criar_corpus.",
                "consulta": consulta,
                "nome_corpus": nome_corpus,
            }

        # Obtém o nome de recurso do corpus
        nome_recurso_corpus = obter_nome_recurso_corpus(nome_corpus)

        # Configura parâmetros de recuperação
        configuracao_recuperacao_rag = rag.RagRetrievalConfig(
            top_k=TOP_K_PADRAO,
            filter=rag.Filter(vector_distance_threshold=THRESHOLD_DISTANCIA_PADRAO),
        )

        # Realiza a consulta
        print("Realizando consulta de recuperação...")
        resposta = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=nome_recurso_corpus,
                )
            ],
            text=consulta,
            rag_retrieval_config=configuracao_recuperacao_rag,
        )

        # Processa a resposta em um formato mais utilizável
        resultados = []
        if hasattr(resposta, "contexts") and resposta.contexts:
            for grupo_ctx in resposta.contexts.contexts:
                resultado = {
                    "uri_origem": (
                        grupo_ctx.source_uri if hasattr(grupo_ctx, "source_uri") else ""
                    ),
                    "nome_origem": (
                        grupo_ctx.source_display_name
                        if hasattr(grupo_ctx, "source_display_name")
                        else ""
                    ),
                    "texto": grupo_ctx.text if hasattr(grupo_ctx, "text") else "",
                    "pontuacao": grupo_ctx.score if hasattr(grupo_ctx, "score") else 0.0,
                }
                resultados.append(resultado)

        # Se não encontrou resultados
        if not resultados:
            return {
                "status": "aviso",
                "mensagem": f"Nenhum resultado encontrado no corpus '{nome_corpus}' para a consulta: '{consulta}'",
                "consulta": consulta,
                "nome_corpus": nome_corpus,
                "resultados": [],
                "contagem_resultados": 0,
            }

        return {
            "status": "sucesso",
            "mensagem": f"Corpus '{nome_corpus}' consultado com sucesso",
            "consulta": consulta,
            "nome_corpus": nome_corpus,
            "resultados": resultados,
            "contagem_resultados": len(resultados),
        }

    except Exception as e:
        mensagem_erro = f"Erro ao consultar corpus: {str(e)}"
        logging.error(mensagem_erro)
        return {
            "status": "erro",
            "mensagem": mensagem_erro,
            "consulta": consulta,
            "nome_corpus": nome_corpus,
        }


def consultar_corpus_rag(
    nome_corpus: str,
    consulta: str,
) -> dict:
    """
    Consulta um corpus RAG do Vertex AI com uma pergunta do usuário e retorna informações relevantes.
    Esta é a função pública que o ADK chama, sem o parâmetro ToolContext.

    Args:
        nome_corpus (str): O nome do corpus a consultar. Se vazio, o corpus atual será usado.
                         Preferencialmente use o resource_name dos resultados de listar_corpora.
        consulta (str): O texto da consulta para buscar no corpus

    Returns:
        dict: Os resultados da consulta e o status
    """
    return _consultar_corpus_rag_impl(nome_corpus, consulta, None)

