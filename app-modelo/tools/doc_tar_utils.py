import os
import requests


def fetch_doc_tar_content(ref_id: str) -> str:
    """
    Busca o conteúdo da TAR/DOC.
    Tenta primeiro via API (futuro), depois localmente como fallback.
    """
    # FUTURO: APIs do Jira e Confluence
    api_urls = {
        "TAR": f"https://gitlab.com/testeagentespoc/teste/-/raw/main/TAR/{ref_id}.txt",
        "DOC": f"https://gitlab.com/testeagentespoc/teste/-/raw/main/DOC/{ref_id}.txt",
    }

    if ref_id.startswith("TAR"):
        url = api_urls["TAR"]
    elif ref_id.startswith("DOC"):
        url = api_urls["DOC"]
    else:
        return "[ERRO] Código inválido."

    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
    except Exception as e:
        pass

    return f"[ERRO] {ref_id} não encontrado nem via API nem localmente."
