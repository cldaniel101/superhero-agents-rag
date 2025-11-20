"""
Ferramenta para recuperar informações detalhadas sobre um corpus RAG específico.
"""

from typing import Optional

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from .utils import verificar_corpus_existe, obter_nome_recurso_corpus


def _obter_info_corpus_impl(
    nome_corpus: str,
    contexto_ferramenta: Optional[ToolContext] = None,
) -> dict:
    """
    Obtém informações detalhadas sobre um corpus RAG específico, incluindo seus arquivos.

    Args:
        nome_corpus (str): O nome de recurso completo do corpus sobre o qual obter informações.
                         Preferencialmente use o resource_name dos resultados de listar_corpora.
        contexto_ferramenta (ToolContext): O contexto da ferramenta

    Returns:
        dict: Informações sobre o corpus e seus arquivos
    """
    try:
        # Verifica se o corpus existe
        if contexto_ferramenta and not verificar_corpus_existe(nome_corpus, contexto_ferramenta):
            return {
                "status": "erro",
                "mensagem": f"O corpus '{nome_corpus}' não existe",
                "nome_corpus": nome_corpus,
            }

        # Obtém o nome de recurso do corpus
        nome_recurso_corpus = obter_nome_recurso_corpus(nome_corpus)

        # Tenta obter detalhes do corpus primeiro
        nome_exibicao_corpus = nome_corpus  # Padrão se não conseguir obter o nome de exibição real

        # Processa informações de arquivo
        detalhes_arquivo = []
        try:
            # Obtém a lista de arquivos
            arquivos = rag.list_files(nome_recurso_corpus)
            for arquivo_rag in arquivos:
                # Obtém detalhes específicos do documento
                try:
                    # Extrai o ID do arquivo do nome
                    id_arquivo = arquivo_rag.name.split("/")[-1]

                    info_arquivo = {
                        "id_arquivo": id_arquivo,
                        "nome_exibicao": (
                            arquivo_rag.display_name
                            if hasattr(arquivo_rag, "display_name")
                            else ""
                        ),
                        "uri_origem": (
                            arquivo_rag.source_uri
                            if hasattr(arquivo_rag, "source_uri")
                            else ""
                        ),
                        "tempo_criacao": (
                            str(arquivo_rag.create_time)
                            if hasattr(arquivo_rag, "create_time")
                            else ""
                        ),
                        "tempo_atualizacao": (
                            str(arquivo_rag.update_time)
                            if hasattr(arquivo_rag, "update_time")
                            else ""
                        ),
                    }

                    detalhes_arquivo.append(info_arquivo)
                except Exception:
                    # Continua para o próximo arquivo
                    continue
        except Exception:
            # Continua sem detalhes de arquivo
            pass

        # Informações básicas do corpus
        return {
            "status": "sucesso",
            "mensagem": f"Informações do corpus '{nome_exibicao_corpus}' recuperadas com sucesso",
            "nome_corpus": nome_corpus,
            "nome_exibicao_corpus": nome_exibicao_corpus,
            "contagem_arquivos": len(detalhes_arquivo),
            "arquivos": detalhes_arquivo,
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao obter informações do corpus: {str(e)}",
            "nome_corpus": nome_corpus,
        }


def obter_info_corpus(
    nome_corpus: str,
) -> dict:
    """
    Obtém informações detalhadas sobre um corpus RAG específico, incluindo seus arquivos.
    Esta é a função pública que o ADK chama, sem o parâmetro ToolContext.

    Args:
        nome_corpus (str): O nome de recurso completo do corpus sobre o qual obter informações.

    Returns:
        dict: Informações sobre o corpus e seus arquivos
    """
    return _obter_info_corpus_impl(nome_corpus, None)

