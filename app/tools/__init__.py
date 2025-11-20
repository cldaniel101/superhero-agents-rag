"""
Pacote de Ferramentas RAG para interagir com corpora RAG do Vertex AI.
"""

from .add_data import adicionar_dados
from .create_corpus import criar_corpus
from .list_corpora import listar_corpora
from .get_corpus_info import obter_info_corpus
from .rag_query import consultar_corpus_rag
from .utils import (
    verificar_corpus_existe,
    obter_nome_recurso_corpus,
    definir_corpus_atual,
)

__all__ = [
    "adicionar_dados",
    "criar_corpus",
    "listar_corpora",
    "consultar_corpus_rag",
    "obter_info_corpus",
    "verificar_corpus_existe",
    "obter_nome_recurso_corpus",
    "definir_corpus_atual",
]

