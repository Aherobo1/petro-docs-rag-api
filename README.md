# PetroDocs RAG API

PetroDocs RAG API is a production-ready FastAPI service featuring a custom Retrieval-Augmented Generation (RAG) pipeline engineered specifically for high-density domain knowledge management. The system automates the ingestion, structural parsing, semantic vectorization, and contextual retrieval of highly specialized petroleum and chemical industry technical documents. 

By binding localized vector storage with large language models, the API translates complex, unstructured technical text into an interactive, grounded knowledgebase chatbot.

### Key Capabilities
* **Advanced Document Parsing:** Specialized multi-format ingestion pipelines handling complex structures across Safety Data Sheets (SDS), Technical Data Sheets (TDS), email exports, and web scraped content.
* **Deterministic RAG Pipeline:** Text chunking powered by LangChain's `RecursiveCharacterTextSplitter` to preserve technical context and table alignment prior to embedding.
* **Vector Architecture:** Local, high-performance semantic search using a persisted ChromaDB database with OpenAI embedding models.
* **Production-Ready Features:** Full API testability via Swagger UI compatibility overrides, real-time web scraping with automated text extraction, and a localized session-based feedback logging loop for model optimization.

## Project Structure

```text
petrodocs_rag_api/
├── main.py
├── requirements.txt
├── .env.example
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── chat.py
│   └── feedback.py
├── chatbot/
│   └── engine.py
├── ingestion/
│   └── pipeline.py
└── README.md
```

Runtime artifacts created by the app and ignored by Git:

- `chroma_db/` - persisted Chroma vector store data.
- `chat_feedback.json` - locally stored session ratings.

## Tech Stack

- FastAPI
- Uvicorn
- LangChain
- ChromaDB
- OpenAI embeddings and chat models
- Pydantic
- python-dotenv
- PyPDF, BeautifulSoup, and Requests for ingestion



## Prerequisites

- Python 3.10 or newer is recommended.
- An OpenAI API key is required for embeddings and answer generation.
- A virtual environment is recommended.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set your values.

## Environment Variables

The example environment file includes:

- `OPENAI_API_KEY` - required by the chatbot engine.
- `ANTHROPIC_API_KEY` - present in the example file, but not used in the current code.
- `CHROMA_PERSIST_DIRECTORY` - vector store location in the example file.
- `QDRANT_URL` and `QDRANT_API_KEY` - present in the example file, but not used in the current code.
- `HOST`, `PORT`, and `DEBUG` - server settings in the example file.

Current implementation details worth noting:

- The Chroma vector store persists to `./chroma_db` in `chatbot/engine.py`.
- The feedback API writes to `chat_feedback.json` in the project root.
- `.gitignore` excludes both of those generated artifacts.

## Running the API

Start the application with Uvicorn:

```bash
uvicorn main:app --reload
```

By default the app is available at `http://127.0.0.1:8000`.

## API Endpoints

### Root

- `GET /` - returns a simple welcome message.

### Chat

- `POST /chat/ask` - asks the chatbot a question.
- `GET /chat/faqs` - returns a generated FAQ list.

Request body for `POST /chat/ask`:

```json
{
  "query": "What is the flash point of Product X?",
  "session_id": "optional-session-id"
}
```

Response fields:

- `query`
- `answer`
- `session_id`
- `sources_used`

### Admin

- `POST /admin/upload` - upload SDS/TDS PDFs, email exports, or other supported documents.
- `POST /admin/scrape` - scrape a website and ingest the text.

`POST /admin/upload` expects multipart form data:

- `files` - one or more files.
- `document_type` - one of `SDS`, `TDS`, or `EMAIL`.

Supported file extensions in the current implementation:

- `.json`
- `.pdf`
- `.txt`
- `.csv`
- `.docx`

`POST /admin/scrape` expects a URL string such as:

```json
"https://example.com"
```

### Feedback

- `POST /feedback/rate` - submit a 1 to 5 star rating for a chatbot session.

Request body:

```json
{
  "session_id": "session-123",
  "rating": 5,
  "feedback": "Helpful and accurate"
}
```

## How The Pipeline Works

1. Content is ingested from files or websites.
2. Text is split into chunks with `RecursiveCharacterTextSplitter`.
3. Chunks are converted into LangChain `Document` objects with source metadata.
4. Documents are stored in Chroma.
5. Chat requests retrieve the top matching chunks.
6. The retrieved context and user question are sent to the chat model to produce an answer.

## Notes

- Website scraping currently disables TLS verification in `ingestion/pipeline.py`.
- The FAQ endpoint currently returns a placeholder FAQ list from the chatbot engine.
- The OpenAPI schema includes a small compatibility fix in `main.py` for Swagger UI file arrays.

## Useful Commands

```bash
uvicorn main:app --reload
pip install -r requirements.txt
```

## License

No license file is present in this repository.
