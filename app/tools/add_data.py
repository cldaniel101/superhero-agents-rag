"""
Ferramenta para adicionar novas fontes de dados a um corpus RAG do Vertex AI.
"""

import re
from typing import List, Optional

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..config import (
    SOBREPOSICAO_CHUNK_PADRAO,
    TAMANHO_CHUNK_PADRAO,
    REQUISICOES_EMBEDDING_POR_MIN_PADRAO,
)
from .utils import verificar_corpus_existe, obter_nome_recurso_corpus


def _adicionar_dados_impl(
    nome_corpus: str,
    caminhos: List[str],
    contexto_ferramenta: Optional[ToolContext] = None,
) -> dict:
    """
    Adiciona novas fontes de dados a um corpus RAG do Vertex AI.

    Args:
        nome_corpus (str): O nome do corpus ao qual adicionar dados. Se vazio, o corpus atual será usado.
        caminhos (List[str]): Lista de URLs ou caminhos GCS para adicionar ao corpus.
                            Formatos suportados:
                            - Google Drive: "https://drive.google.com/file/d/{FILE_ID}/view"
                            - Google Docs/Sheets/Slides: "https://docs.google.com/{type}/d/{FILE_ID}/..."
                            - Google Cloud Storage: "gs://{BUCKET}/{PATH}"
                            Exemplo: ["https://drive.google.com/file/d/123", "gs://meu_bucket/meus_arquivos_dir"]
        contexto_ferramenta (ToolContext): O contexto da ferramenta

    Returns:
        dict: Informações sobre os dados adicionados e status
    """
    # Verifica se o corpus existe
    if contexto_ferramenta and not verificar_corpus_existe(nome_corpus, contexto_ferramenta):
        return {
            "status": "erro",
            "mensagem": f"O corpus '{nome_corpus}' não existe. Por favor, crie-o primeiro usando a ferramenta criar_corpus.",
            "nome_corpus": nome_corpus,
            "caminhos": caminhos,
        }

    # Valida entradas
    if not caminhos or not all(isinstance(caminho, str) for caminho in caminhos):
        return {
            "status": "erro",
            "mensagem": "Caminhos inválidos: Por favor, forneça uma lista de URLs ou caminhos GCS",
            "nome_corpus": nome_corpus,
            "caminhos": caminhos,
        }

    # Pré-processa caminhos para validar e converter URLs do Google Docs para formato Drive, se necessário
    caminhos_validados = []
    caminhos_invalidos = []
    conversoes = []

    for caminho in caminhos:
        if not caminho or not isinstance(caminho, str):
            caminhos_invalidos.append(f"{caminho} (Não é uma string válida)")
            continue

        # Verifica URLs do Google Docs/Sheets/Slides e converte para formato Drive, se necessário
        match_docs = re.match(
            r"https:\/\/docs\.google\.com\/(?:document|spreadsheets|presentation)\/d\/([a-zA-Z0-9_-]+)(?:\/|$)",
            caminho,
        )
        if match_docs:
            file_id = match_docs.group(1)
            url_drive = f"https://drive.google.com/file/d/{file_id}/view"
            caminhos_validados.append(url_drive)
            conversoes.append(f"{caminho} → {url_drive}")
            continue

        # Verifica formato de URL do Drive válido
        match_drive = re.match(
            r"https:\/\/drive\.google\.com\/(?:file\/d\/|open\?id=)([a-zA-Z0-9_-]+)(?:\/|$)",
            caminho,
        )
        if match_drive:
            # Normaliza para o formato padrão de URL do Drive
            file_id = match_drive.group(1)
            url_drive = f"https://drive.google.com/file/d/{file_id}/view"
            caminhos_validados.append(url_drive)
            if url_drive != caminho:
                conversoes.append(f"{caminho} → {url_drive}")
            continue

        # Verifica caminhos GCS
        if caminho.startswith("gs://"):
            caminhos_validados.append(caminho)
            continue

        # Se chegou aqui, o caminho não estava em um formato reconhecido
        caminhos_invalidos.append(f"{caminho} (Formato inválido)")

    # Verifica se temos caminhos válidos após validação
    if not caminhos_validados:
        return {
            "status": "erro",
            "mensagem": "Nenhum caminho válido fornecido. Por favor, forneça URLs do Google Drive ou caminhos GCS.",
            "nome_corpus": nome_corpus,
            "caminhos_invalidos": caminhos_invalidos,
        }

    try:
        # Obtém o nome de recurso do corpus
        nome_recurso_corpus = obter_nome_recurso_corpus(nome_corpus)

        # Configura configuração de chunking
        configuracao_transformacao = rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=TAMANHO_CHUNK_PADRAO,
                chunk_overlap=SOBREPOSICAO_CHUNK_PADRAO,
            ),
        )

        # Importa arquivos para o corpus
        resultado_importacao = rag.import_files(
            nome_recurso_corpus,
            caminhos_validados,
            transformation_config=configuracao_transformacao,
            max_embedding_requests_per_min=REQUISICOES_EMBEDDING_POR_MIN_PADRAO,
        )

        # Define este como o corpus atual se ainda não estiver definido
        if contexto_ferramenta and not contexto_ferramenta.state.get("corpus_atual"):
            contexto_ferramenta.state["corpus_atual"] = nome_corpus

        # Constrói a mensagem de sucesso
        mensagem_conversao = ""
        if conversoes:
            mensagem_conversao = " (URLs do Google Docs convertidas para formato Drive)"

        return {
            "status": "sucesso",
            "mensagem": f"Adicionado(s) {resultado_importacao.imported_rag_files_count} arquivo(s) ao corpus '{nome_corpus}'{mensagem_conversao}",
            "nome_corpus": nome_corpus,
            "arquivos_adicionados": resultado_importacao.imported_rag_files_count,
            "caminhos": caminhos_validados,
            "caminhos_invalidos": caminhos_invalidos,
            "conversoes": conversoes,
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao adicionar dados ao corpus: {str(e)}",
            "nome_corpus": nome_corpus,
            "caminhos": caminhos,
        }


def adicionar_dados(
    nome_corpus: str,
    caminhos: List[str],
) -> dict:
    """
    Adiciona novas fontes de dados a um corpus RAG do Vertex AI.
    Esta é a função pública que o ADK chama, sem o parâmetro ToolContext.

    Args:
        nome_corpus (str): O nome do corpus ao qual adicionar dados. Se vazio, o corpus atual será usado.
        caminhos (List[str]): Lista de URLs ou caminhos GCS para adicionar ao corpus.

    Returns:
        dict: Informações sobre os dados adicionados e status
    """
    return _adicionar_dados_impl(nome_corpus, caminhos, None)

