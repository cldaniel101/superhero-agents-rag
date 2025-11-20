# Configurando a Vertex

Aqui está um **passo a passo completo** para você guiar os alunos na criação de um corpus usando Vertex AI RAG Engine no Google Cloud Vertex AI. Vou detalhar cada etapa com comandos, links, e dicas pra tornar simples.

---

## Passos para criar o corpus

### 1. Preparar o projeto no GCP

- Acesse o console do Google Cloud e selecione/crie um **Projeto**.
- Ative a API da Vertex AI:
    - No menu “APIs & Serviços” → “Biblioteca” → procure por *Vertex AI* e habilite.
- Opcional: defina a região (por exemplo `us-central1`) para os recursos.
    - Atenção: há relatos de que algumas regiões têm limitações para RAG. ([Google Developer forums](https://discuss.google.dev/t/vertexai-rag-engine-does-not-work-in-europe/192386?utm_source=chatgpt.com))

### 2. Conceder permissões ao usuário

Execute no Cloud Shell ou terminal local com `gcloud`:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \\
  --member="user:YOUR_EMAIL" \\
  --role="roles/aiplatform.user"

```

- Substitua `PROJECT_ID` pelo ID do seu projeto.
- Substitua `YOUR_EMAIL` pelo e-mail do aluno/instrutor.
([Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart?hl=pt&utm_source=chatgpt.com))
- Isso garante que o usuário pode usar a Vertex AI.
- Se for necessário acesso ao Cloud Storage, também pode dar `roles/storage.objectAdmin`.

### 3. Configurar credenciais locais (para código Python)

No terminal:

```bash
gcloud config set project PROJECT_ID
gcloud auth application-default login

```

- Isso configura o CLI `gcloud` para apontar ao seu projeto. ([Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart?hl=pt&utm_source=chatgpt.com))
- Instale o SDK Python da Vertex AI:

```bash
pip install google-cloud-aiplatform

```

### 4. Criar o corpus via SDK Python

Aqui vai o script mínimo (alunos podem rodar em Notebook ou VSCode):

```python
from vertexai import rag
import vertexai

PROJECT_ID = "seu-projeto"
LOCATION = "us-central1"  # ou região suportada
DISPLAY_NAME = "meu_corpus_exemplo"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Configurar modelo de embedding
embedding_model_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
        publisher_model="publishers/google/models/text-embedding-005"
    )
)

# Criar o corpus
rag_corpus = rag.create_corpus(
    display_name=DISPLAY_NAME,
    backend_config=rag.RagVectorDbConfig(
        rag_embedding_model_config=embedding_model_config
    ),
)
print("Corpus criado:", rag_corpus.name)

```

- Esse código segue o exemplo oficial. ([Google Cloud Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart?utm_source=chatgpt.com))
- Anote o valor `rag_corpus.name` — você vai usar depois.

### 5. Importar documentos para o corpus

Suponha que você tenha um bucket no Google Cloud Storage (`gs://meu-bucket/doc1.pdf`) ou links do Google Drive.

```python
paths = [
    "gs://meu-bucket/doc1.pdf",
    "gs://meu-bucket/doc2.txt"
    # ou links do Drive como "<https://drive.google.com/file/d/>..."
]

rag.import_files(
    rag_corpus.name,
    paths,
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(
            chunk_size=512,
            chunk_overlap=100
        )
    ),
    max_embedding_requests_per_min=1000,
)
print("Arquivos importados para o corpus.")

```

- `chunk_size` e `chunk_overlap` determinam como o sistema divide o texto para indexação. ([Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart?hl=pt&utm_source=chatgpt.com))
- Aguarde alguns minutos — a criação e indexação pode demorar. ([Google Cloud Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/manage-your-rag-corpus?utm_source=chatgpt.com))

### 6. Verificar/importar status (opcional)

Você pode listar os arquivos no corpus ou verificar o status da importação. Na documentação: “List RAG files” etc. ([Google Cloud Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/manage-your-rag-corpus?utm_source=chatgpt.com))

### 7. Usar o corpus para recuperação ou geração

Depois da indexação, você pode fazer uma consulta direta para ver se está funcionando:

```python
rag_retrieval_config = rag.RagRetrievalConfig(
    top_k=3,
    filter=rag.Filter(vector_distance_threshold=0.5)
)

response = rag.retrieval_query(
    rag_resources=[rag.RagResource(rag_corpus=rag_corpus.name)],
    text="O que este material diz sobre Waving App?",
    rag_retrieval_config=rag_retrieval_config
)

print("Trechos encontrados:", response)

```

- Esse trecho mostra que o seu corpus está ativo e recuperando conteúdo. ([Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart?hl=pt&utm_source=chatgpt.com))
- Depois, no seu agente ADK, você usará esse corpus em `VertexAiRagRetrieval`.

### 8. Limpeza (opcional mas para aula pode mencionar)

Para não manter recursos ociosos, você pode deletar o corpus:

```python
rag.delete_corpus(rag_corpus.name)
print("Corpus deletado.")

```

([Medium](https://medium.com/google-cloud/building-vertex-ai-rag-engine-with-gemini-2-flash-llm-79c27445dd48?utm_source=chatgpt.com))

---

## 📝 Dicas rápidas para a turma

- Escolha uma **região suportada** — se usarem Europa pode dar erro. ([Google Developer forums](https://discuss.google.dev/t/vertexai-rag-engine-does-not-work-in-europe/192386?utm_source=chatgpt.com))
- Tenha os documentos prontos (PDFs, TXT) antes da aula, para não perder tempo.
- Explique o que são “chunk_size” e “chunk_overlap” com analogia: “quebra o livro em páginas menores que o agente consegue ‘ler’ melhor”.
- Monitore o tempo de indexação — em aula ao vivo talvez esperar ~2-5min.
- Mostre o ID do corpus criado (`rag_corpus.name`) porque os alunos vão usá-lo no código do agente.

---

Se quiser, posso gerar **um slide rápido (em PowerPoint-ou-Google Slides)** já pronto para você usar nesta parte “criar o corpus” — com screenshots, checklist de passos, e espaço para os alunos preencherem. Quer que eu monte?