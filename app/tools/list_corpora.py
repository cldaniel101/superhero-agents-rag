"""
Ferramenta para listar todos os corpora RAG do Vertex AI disponíveis.
"""

from typing import Dict, List, Union

from vertexai import rag


def listar_corpora() -> dict:
    """
    Lista todos os corpora RAG do Vertex AI disponíveis.

    Returns:
        dict: Uma lista de corpora disponíveis e status, com cada corpus contendo:
            - nome_recurso: O nome de recurso completo para usar com outras ferramentas
            - nome_exibicao: O nome legível do corpus
            - tempo_criacao: Quando o corpus foi criado
            - tempo_atualizacao: Quando o corpus foi atualizado pela última vez
    """
    try:
        # Obtém a lista de corpora
        corpora = rag.list_corpora()

        # Processa informações do corpus em um formato mais utilizável
        info_corpus: List[Dict[str, Union[str, int]]] = []
        for corpus in corpora:
            dados_corpus: Dict[str, Union[str, int]] = {
                "nome_recurso": corpus.name,  # Nome de recurso completo para uso com outras ferramentas
                "nome_exibicao": corpus.display_name,
                "tempo_criacao": (
                    str(corpus.create_time) if hasattr(corpus, "create_time") else ""
                ),
                "tempo_atualizacao": (
                    str(corpus.update_time) if hasattr(corpus, "update_time") else ""
                ),
            }

            info_corpus.append(dados_corpus)

        return {
            "status": "sucesso",
            "mensagem": f"Encontrados {len(info_corpus)} corpora disponíveis",
            "corpora": info_corpus,
        }
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao listar corpora: {str(e)}",
            "corpora": [],
        }

