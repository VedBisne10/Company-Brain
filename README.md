# Company Brain

**A unified organizational knowledge graph powered by FastAPI, FalkorDB, GitHub, Slack, Google Drive/Docs, and LLM-powered Retrieval-Augmented Generation (RAG).**

Company Brain brings company knowledge from code repositories, team conversations, and documents into one connected system. It aims to help people find information, understand relationships, discover decisions, and answer questions with relevant supporting context.

> **Project status:** Architecture and implementation scaffold. Update this section as integrations and features become operational. Do not describe a feature as complete until it has been implemented and tested.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals](#2-goals)
3. [Technology Stack](#3-technology-stack)
4. [Architecture at a Glance](#4-architecture-at-a-glance)
5. [Repository Structure](#5-repository-structure)
6. [Backend Folder Guide](#6-backend-folder-guide)
7. [Frontend Folder Guide](#7-frontend-folder-guide)
8. [Data and Scripts](#8-data-and-scripts)
9. [How Data Flows Through the System](#9-how-data-flows-through-the-system)
10. [Knowledge Graph Design](#10-knowledge-graph-design)
11. [RAG and LLM Flow](#11-rag-and-llm-flow)
12. [API Responsibilities](#12-api-responsibilities)
13. [Environment Configuration](#13-environment-configuration)
14. [Local Development Setup](#14-local-development-setup)
15. [Implementation Order](#15-implementation-order)
16. [Testing](#16-testing)
17. [Security and Privacy](#17-security-and-privacy)
18. [Git and `.gitignore`](#18-git-and-gitignore)
19. [Team Responsibilities](#19-team-responsibilities)
20. [Troubleshooting](#20-troubleshooting)
21. [Contributing](#21-contributing)
22. [Roadmap](#22-roadmap)

---

## 1. Project Overview

Organizations store knowledge across multiple tools:

- **GitHub:** repositories, pull requests, issues, commits, code reviews, and releases.
- **Slack:** messages, threads, channels, and team discussions.
- **Google Drive/Docs:** design documents, meeting notes, specifications, and decisions.
- **FalkorDB:** a graph database used to connect people, projects, messages, documents, code artifacts, and decisions.
- **LLM + RAG:** retrieve relevant information and generate answers grounded in the retrieved context.
- **FastAPI:** backend API that exposes chat, search, graph, integration, and webhook functionality.
- **Frontend:** user interface for asking questions, exploring the knowledge graph, and managing integrations.

Company Brain is intended to connect these sources instead of treating every platform as a separate information silo.

### Example use case

A user asks:

> Why did the team choose OAuth for the authentication service, and who worked on it?

Company Brain could retrieve a relevant Slack discussion, a Google architecture document, and GitHub pull requests, connect them to the authentication project and contributors, and ask the LLM to produce a sourced answer.

The answer should distinguish retrieved evidence from inference and provide links to original sources whenever possible.

---

## 2. Goals

1. **Unified knowledge:** represent information from multiple platforms in a common internal format.
2. **Connected context:** model relationships between people, projects, repositories, issues, messages, documents, and decisions.
3. **Semantic retrieval:** find relevant content even when the question uses different wording from the source.
4. **Graph-aware retrieval:** use relationships to answer questions involving ownership, dependencies, contributors, and decisions.
5. **Grounded answers:** generate answers from retrieved evidence and show source references.
6. **Maintainable integrations:** keep each external provider separate from the graph and AI layers.
7. **Incremental synchronization:** update existing entities and process repeated events without creating unnecessary duplicates.

### Non-goals for the initial version

- Replacing GitHub, Slack, or Google Drive.
- Automatically treating every generated conclusion as an established fact.
- Bypassing permissions on connected platforms.
- Requiring every possible integration or advanced agent capability before the first working demo.

---

## 3. Technology Stack

| Component | Technology | Responsibility |
|---|---|---|
| Backend API | FastAPI | HTTP APIs, request validation, webhook endpoints |
| Graph database | FalkorDB | Knowledge entities and their relationships |
| GitHub integration | GitHub API and webhooks | Repository and collaboration data |
| Slack integration | Slack API and events | Conversations and message data |
| Google integration | Google Drive API and Google Docs API | Files and document content |
| LLM | Configured LLM provider | Generate answers from retrieved context |
| Embeddings | Configured embedding model | Represent text for semantic similarity search |
| Retrieval | Graph + vector/hybrid RAG | Find relevant evidence |
| Frontend | React-based frontend (if using the scaffold in this repository) | Chat, search, graph, and integration UI |
| Containers | Docker / Docker Compose | Repeatable local and deployment environments |
| Tests | pytest and frontend test tooling as configured | Validate behavior and integration contracts |

The specific LLM provider, embedding model, vector-search implementation, and frontend libraries should be selected and recorded in the actual configuration. The folder structure alone does not imply that these dependencies are already implemented.

---

## 4. Architecture at a Glance

```text
 GitHub             Slack             Google Drive / Docs
    |                  |                       |
    +------------------+-----------------------+
                       |
              Provider integrations
                       |
               Parse and normalize
                       |
                 Ingestion pipeline
                       |
              Graph builder / repository
                       |
                    FalkorDB
              /                     \
      Graph retrieval          Vector retrieval
              \                     /
                Hybrid retrieval
                       |
               Context construction
                       |
                    LLM / RAG
                       |
                  Chat service
                       |
                    FastAPI
                       |
                    Frontend
```

**Important separation of responsibilities:**

- Integration modules communicate with external providers and translate provider-specific payloads.
- Ingestion modules normalize, chunk, deduplicate, and coordinate ingestion.
- Graph modules own FalkorDB access and graph persistence.
- RAG modules retrieve and prepare evidence.
- LLM modules manage model interaction, prompts, and answer formatting.
- Services coordinate business workflows.
- API routes handle HTTP requests and responses; they should not contain large amounts of business logic.

---

## 5. Repository Structure

The following is the intended repository layout. Some files may be added as implementation progresses.

```text
company-brain/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── search.py
│   │   │   │   ├── graph.py
│   │   │   │   └── integrations.py
│   │   │   └── webhooks/
│   │   │       ├── github.py
│   │   │       ├── slack.py
│   │   │       └── google.py
│   │   ├── integrations/
│   │   │   ├── github/
│   │   │   │   ├── client.py
│   │   │   │   ├── parser.py
│   │   │   │   ├── mapper.py
│   │   │   │   └── events.py
│   │   │   ├── slack/
│   │   │   │   ├── client.py
│   │   │   │   ├── parser.py
│   │   │   │   ├── mapper.py
│   │   │   │   └── events.py
│   │   │   └── google/
│   │   │       ├── drive.py
│   │   │       ├── docs.py
│   │   │       ├── parser.py
│   │   │       └── mapper.py
│   │   ├── ingestion/
│   │   │   ├── pipeline.py
│   │   │   ├── normalizer.py
│   │   │   ├── chunker.py
│   │   │   └── deduplicator.py
│   │   ├── graph/
│   │   │   ├── client.py
│   │   │   ├── schema.py
│   │   │   ├── queries.py
│   │   │   ├── repository.py
│   │   │   ├── builder.py
│   │   │   └── embeddings.py
│   │   ├── rag/
│   │   │   ├── retriever.py
│   │   │   ├── graph_retriever.py
│   │   │   ├── vector_retriever.py
│   │   │   ├── hybrid_retriever.py
│   │   │   ├── reranker.py
│   │   │   ├── context_builder.py
│   │   │   └── pipeline.py
│   │   ├── llm/
│   │   │   ├── client.py
│   │   │   ├── prompts.py
│   │   │   ├── agent.py
│   │   │   └── response.py
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   ├── search_service.py
│   │   │   ├── graph_service.py
│   │   │   └── integration_service.py
│   │   ├── models/
│   │   │   ├── common.py
│   │   │   ├── github.py
│   │   │   ├── slack.py
│   │   │   ├── google.py
│   │   │   ├── graph.py
│   │   │   └── chat.py
│   │   └── utils/
│   │       ├── logger.py
│   │       ├── security.py
│   │       ├── hashing.py
│   │       └── helpers.py
│   ├── tests/
│   │   ├── integrations/
│   │   ├── test_ingestion.py
│   │   ├── test_graph.py
│   │   ├── test_rag.py
│   │   └── test_chat.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   ├── Graph/
│   │   │   ├── Search/
│   │   │   └── Integrations/
│   │   ├── pages/
│   │   │   ├── Dashboard/
│   │   │   ├── Chat/
│   │   │   ├── KnowledgeGraph/
│   │   │   └── Integrations/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
├── scripts/
│   ├── seed_graph.py
│   ├── ingest_github.py
│   ├── ingest_slack.py
│   ├── ingest_google.py
│   └── rebuild_graph.py
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── docker-compose.yml
├── .gitignore
├── .env.example
├── README.md
└── LICENSE
```

Python package directories may also contain `__init__.py` files. Add them wherever needed for your package/import strategy.

---

## 6. Backend Folder Guide

The backend lives in `backend/`. Its application code lives in `backend/app/`.

### 6.1 `main.py` — application entry point

Creates the FastAPI application, configures lifespan/startup and shutdown behavior, and registers routers and middleware.

Typical responsibilities:

- Create the `FastAPI` instance.
- Register route and webhook routers.
- Configure CORS for the approved frontend origin.
- Initialize and close shared clients through application lifespan where appropriate.
- Expose API metadata and health endpoints through their routers.

Keep provider-specific logic and graph queries out of `main.py`.

### 6.2 `config/settings.py` — configuration

Loads and validates environment-based settings, such as database connection information, provider credentials, LLM settings, and application environment.

Use typed settings and fail clearly when a required setting is missing. Never hardcode secrets in source code.

### 6.3 `api/routes/` — frontend-facing API

These modules define request and response contracts for the user interface.

| File | Responsibility |
|---|---|
| `health.py` | Liveness/readiness endpoints and dependency health checks as appropriate |
| `chat.py` | Accept questions and return generated answers with source references |
| `search.py` | Search ingested content and return relevant results |
| `graph.py` | Expose safe graph exploration and entity/relationship queries |
| `integrations.py` | Report connection and synchronization status; initiate permitted sync actions |

Routes should validate input, call a service, and return a response. They should not implement the entire RAG or ingestion pipeline themselves.

### 6.4 `api/webhooks/` — incoming events

These endpoints receive provider events. They must verify provider signatures or request authenticity, validate the event, and handle retries safely.

| File | Responsibility |
|---|---|
| `github.py` | Receive and validate supported GitHub webhook events |
| `slack.py` | Handle Slack URL verification and supported event callbacks |
| `google.py` | Handle Google-related callbacks only if the chosen Google API flow uses them |

Not every Google Drive/Docs synchronization flow requires a webhook endpoint. Polling or scheduled synchronization may be more appropriate for the initial implementation.

Webhook handlers should return promptly. For slower work, enqueue a job or hand the event to a background worker rather than keeping the provider's request open.

### 6.5 `integrations/` — provider-specific communication

Each provider gets its own module so that provider-specific schemas and API behavior do not leak into the rest of the system.

#### `integrations/github/`

- `client.py`: API client and pagination/rate-limit handling.
- `parser.py`: Parse GitHub payloads into clean provider-specific records.
- `mapper.py`: Map provider records to the application's common knowledge representation.
- `events.py`: Dispatch and interpret supported event types.

Potential initial entities include repositories, users, pull requests, issues, comments, commits, and releases. Only ingest what is required and authorized.

#### `integrations/slack/`

- `client.py`: Slack API calls, pagination, and retry handling.
- `parser.py`: Parse events, messages, threads, and channel metadata.
- `mapper.py`: Map Slack records into common knowledge objects.
- `events.py`: Handle supported event types and filter irrelevant or unsupported events.

Slack access must respect workspace installation, scopes, channel access, and privacy expectations. Do not assume the application can read every private channel.

#### `integrations/google/`

- `drive.py`: Find files, inspect metadata, and download/export supported content.
- `docs.py`: Read Google Docs content and extract supported structural elements.
- `parser.py`: Normalize document text, sections, metadata, and links.
- `mapper.py`: Map files and document content into the common knowledge model.

Use OAuth scopes appropriate to the required functionality. Store refresh/access tokens securely; do not commit credential files or tokens.

### 6.6 `ingestion/` — normalize and prepare content

This layer turns provider-specific records into consistent, deduplicated knowledge.

| File | Responsibility |
|---|---|
| `pipeline.py` | Orchestrate validation, normalization, chunking, and persistence |
| `normalizer.py` | Convert provider records into common knowledge objects |
| `chunker.py` | Split long content into useful chunks for retrieval |
| `deduplicator.py` | Use stable source IDs and hashes to detect duplicates and changes |

The common representation should preserve source identity, timestamps, source URL, author when available, permissions/visibility metadata where needed, content, and entity relationships.

Ingestion should be **idempotent**: receiving the same event twice should not create duplicate nodes or relationships. Updates should change existing records when appropriate.

### 6.7 `graph/` — FalkorDB persistence and graph model

| File | Responsibility |
|---|---|
| `client.py` | Create and manage the FalkorDB connection/client |
| `schema.py` | Document entity labels, relationship types, and expected properties |
| `queries.py` | Keep reusable, parameterized Cypher queries |
| `repository.py` | Provide persistence and query methods to services |
| `builder.py` | Convert normalized objects into nodes and relationships |
| `embeddings.py` | Coordinate embedding-related storage or graph/vector indexing where supported |

Keep the connection lifecycle in one place. Use parameterized queries and validate labels or relationship types rather than inserting untrusted strings into Cypher.

FalkorDB is the structured relationship store. If vector search is used, implement it using the capabilities supported by the selected FalkorDB version and configuration, or choose a separate vector store deliberately. Do not assume that a file named `embeddings.py` automatically provides vector indexing.

### 6.8 `rag/` — retrieval and context preparation

| File | Responsibility |
|---|---|
| `retriever.py` | Define a common retrieval interface or coordinate retrieval |
| `graph_retriever.py` | Find entities and related information through graph traversal |
| `vector_retriever.py` | Retrieve semantically similar text chunks |
| `hybrid_retriever.py` | Combine graph and vector retrieval results |
| `reranker.py` | Reorder candidates by relevance if a reranker is configured |
| `context_builder.py` | Build a compact, source-aware context for the LLM |
| `pipeline.py` | Orchestrate retrieval, ranking, context construction, and generation |

A simple first version can use graph traversal and keyword search before adding vector retrieval and reranking. Add complexity only when it improves answer quality.

### 6.9 `llm/` — model interaction

| File | Responsibility |
|---|---|
| `client.py` | Wrap the selected LLM provider and its API |
| `prompts.py` | Store system prompts and task-specific templates |
| `agent.py` | Coordinate tool selection or multi-step reasoning, if needed |
| `response.py` | Validate/format generated answers and source references |

The LLM should receive only the context needed to answer a question. Treat retrieved messages and documents as untrusted content, not as instructions that override the system prompt. Require answers to cite retrieved evidence and allow the model to say when evidence is insufficient.

### 6.10 `services/` — application workflows

Services connect API requests to the appropriate integrations, graph operations, and RAG functions.

- `chat_service.py`: runs the question-answering workflow.
- `search_service.py`: performs search and formats results.
- `graph_service.py`: retrieves entities, neighbors, and graph summaries.
- `integration_service.py`: manages integration status and synchronization workflows.

Keep service functions testable and avoid coupling them directly to HTTP request objects.

### 6.11 `models/` — typed data contracts

Use Pydantic models or other clearly defined types for:

- Provider payloads and normalized records.
- Chat request/response bodies.
- Graph entities and relationships.
- Search results and citations.
- Integration status and sync results.

Provider models describe provider data; common models describe your internal contract. Keeping them separate makes provider API changes easier to manage.

### 6.12 `utils/` — shared utilities

- `logger.py`: consistent structured logging.
- `security.py`: signature verification and security helpers.
- `hashing.py`: deterministic content hashes for change detection.
- `helpers.py`: small generic functions used by multiple modules.

Avoid turning `utils/` into a miscellaneous folder for core application logic.

---

## 7. Frontend Folder Guide

The frontend provides the user-facing experience. It communicates with FastAPI and should not connect directly to FalkorDB or provider APIs using privileged credentials.

### `components/`

Reusable UI elements grouped by feature:

- `Chat/`: question input, answer display, source citations, loading and error states.
- `Graph/`: graph canvas, nodes, edges, and entity detail panel.
- `Search/`: search box, filters, and result cards.
- `Integrations/`: provider connection status, sync status, and setup guidance.

### `pages/`

Top-level screens:

- `Dashboard/`: overview and recent activity.
- `Chat/`: ask questions about company knowledge.
- `KnowledgeGraph/`: explore connected entities and relationships.
- `Integrations/`: view and manage connected sources.

### `services/api.js`

Central place for frontend HTTP requests to FastAPI. Configure the backend base URL through a frontend environment variable. Handle API errors and request timeouts consistently.

### `hooks/`

Reusable frontend state and behavior, such as fetching graph data, managing chat state, or polling integration status.

### `utils/`

Small frontend helpers such as date formatting and display utilities.

### `App.jsx` and `main.jsx`

`main.jsx` bootstraps the frontend. `App.jsx` defines the main application layout and routing, depending on the frontend framework setup.

---

## 8. Data and Scripts

### 8.1 `data/`

```text
data/
├── raw/
├── processed/
└── embeddings/
```

- `raw/`: optional local copies of original provider payloads for debugging or replay.
- `processed/`: optional normalized records or intermediate artifacts.
- `embeddings/`: optional locally generated embedding artifacts.

These directories are for development workflows, not the canonical knowledge store. Company data can be confidential, so local data should normally remain out of Git. Use synthetic examples for tests and demos.

### 8.2 `scripts/`

- `seed_graph.py`: populate the graph with synthetic demo data or a controlled seed dataset.
- `ingest_github.py`: run an initial/manual GitHub ingestion.
- `ingest_slack.py`: run an initial/manual Slack ingestion.
- `ingest_google.py`: run an initial/manual Google Drive/Docs ingestion.
- `rebuild_graph.py`: rebuild graph data from a known source, with safeguards.

Scripts should reuse the same integration, normalization, and repository functions as the API. Avoid maintaining a separate, inconsistent ingestion implementation in each script.

Before running a rebuild, confirm the target graph and data source. Destructive reset operations should require an explicit flag and clear warning.

---

## 9. How Data Flows Through the System

### 9.1 GitHub ingestion

```text
GitHub webhook or API sync
          |
          v
api/webhooks/github.py or scripts/ingest_github.py
          |
          v
integrations/github/
          |
          v
ingestion/normalizer.py
          |
          v
ingestion/deduplicator.py
          |
          v
graph/builder.py
          |
          v
graph/repository.py
          |
          v
FalkorDB
```

### 9.2 Slack ingestion

```text
Slack event or API sync
          |
          v
api/webhooks/slack.py or scripts/ingest_slack.py
          |
          v
integrations/slack/
          |
          v
Ingestion pipeline
          |
          v
FalkorDB
```

### 9.3 Google Drive/Docs ingestion

```text
Drive listing/change sync
          |
          v
integrations/google/drive.py
          |
          v
Google Docs content extraction
          |
          v
Parser and normalizer
          |
          v
Chunking and optional embedding generation
          |
          v
Graph persistence and configured vector index
```

The exact sync strategy depends on the provider APIs, scopes, and deployment model. Use webhooks where supported and useful, and periodic sync for initial backfills or missed changes.

### 9.4 Question answering

```text
User question
     |
     v
POST /api/chat
     |
     v
services/chat_service.py
     |
     v
rag/pipeline.py
     |
     +------------------+
     |                  |
     v                  v
Graph retrieval     Vector retrieval
     |                  |
     +---------+--------+
               |
               v
      Merge / optional rerank
               |
               v
       Context builder
               |
               v
           LLM client
               |
               v
   Answer + source references
               |
               v
          Frontend
```

---

## 10. Knowledge Graph Design

FalkorDB represents entities as nodes and their connections as relationships. A starting ontology might include:

### Node labels

- `Person`
- `Team`
- `Project`
- `Repository`
- `PullRequest`
- `Issue`
- `Commit`
- `SlackChannel`
- `SlackMessage`
- `Document`
- `Chunk`
- `Decision`
- `Task`

Add labels only when they support a real use case. Avoid making the schema more complex than the data and queries require.

### Example relationships

```text
(Person)-[:WORKS_ON]->(Project)
(Person)-[:AUTHORED]->(PullRequest)
(PullRequest)-[:BELONGS_TO]->(Repository)
(Person)-[:SENT]->(SlackMessage)
(SlackMessage)-[:IN_CHANNEL]->(SlackChannel)
(Document)-[:RELATED_TO]->(Project)
(Document)-[:CONTAINS]->(Chunk)
(SlackMessage)-[:MENTIONS]->(Person)
(Decision)-[:ABOUT]->(Project)
```

These are illustrative relationships, not a complete enforced schema. Choose relationship direction and names consistently in `graph/schema.py`.

### Recommended common properties

Where relevant, entities should preserve:

- Stable internal ID.
- Provider/source name.
- Stable provider-specific ID.
- Title or display name.
- Content or summary.
- Source URL.
- Author or creator ID.
- Created/updated timestamps.
- Content hash or version information.
- Visibility/permission metadata needed for access control.

Use stable provider IDs to avoid duplicates. Do not merge people solely because their display names match; use reliable identifiers and explicit identity-resolution rules.

### Source traceability

Every retrieved piece of evidence should be traceable to its original source, such as a GitHub PR URL, Slack permalink, or Google Drive/Docs URL. Store timestamps and source identifiers so the application can explain where an answer came from.

---

## 11. RAG and LLM Flow

Retrieval-Augmented Generation (RAG) retrieves relevant evidence and supplies it to an LLM before answer generation.

1. **Receive the question:** validate the request and any tenant/user scope.
2. **Retrieve graph context:** find relevant entities and relationships.
3. **Retrieve text context:** use vector or keyword search over authorized chunks.
4. **Combine candidates:** remove duplicates and preserve source metadata.
5. **Rerank when needed:** prioritize the most relevant evidence.
6. **Build context:** fit the strongest evidence within the model's context budget.
7. **Generate an answer:** instruct the LLM to answer from evidence, cite sources, and disclose uncertainty.
8. **Return a structured response:** include the answer and source references.

A useful response contract could look like this:

```json
{
  "answer": "The team selected OAuth based on the retrieved design discussion.",
  "sources": [
    {
      "source_type": "github",
      "title": "Authentication implementation",
      "url": "https://example.com/source",
      "excerpt": "Illustrative excerpt from retrieved content"
    }
  ],
  "insufficient_evidence": false
}
```

This is an example response shape, not a promise that the endpoint has already been implemented. Replace example URLs and text with real authorized source data.

**Important:** embeddings provide semantic similarity, not proof that a claim is true. Graph relationships provide structure, not automatic certainty. Answers should be grounded in source evidence and should not invent missing decisions or ownership.

---

## 12. API Responsibilities

The following routes are a suggested API contract. Confirm the actual registered paths in the FastAPI app as implementation proceeds.

| Method | Suggested path | Purpose |
|---|---|---|
| `GET` | `/health` | Basic liveness check |
| `GET` | `/api/integrations` | List integration status |
| `POST` | `/api/integrations/{provider}/sync` | Start a permitted sync |
| `POST` | `/api/chat` | Ask a question |
| `GET` | `/api/search?q=...` | Search knowledge |
| `GET` | `/api/graph/entities/{entity_id}` | Retrieve an entity |
| `GET` | `/api/graph/entities/{entity_id}/neighbors` | Retrieve related graph entities |
| `POST` | `/webhooks/github` | Receive GitHub events |
| `POST` | `/webhooks/slack` | Receive Slack events |
| `POST` | `/webhooks/google` | Optional Google callback endpoint |

These are design recommendations. A route is available only after it is implemented and registered.

FastAPI typically provides interactive API documentation at `/docs` and an alternative schema view at `/redoc` when enabled.

---

## 13. Environment Configuration

Create local environment files from the templates. Keep real secrets out of Git.

Example root `.env.example`:

```dotenv
APP_ENV=development
LOG_LEVEL=INFO

# FalkorDB
FALKORDB_HOST=localhost
FALKORDB_PORT=6379
FALKORDB_PASSWORD=
FALKORDB_GRAPH_NAME=company_brain

# GitHub
GITHUB_TOKEN=
GITHUB_WEBHOOK_SECRET=

# Slack
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=

# Google Drive / Docs
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_CREDENTIALS_FILE=

# LLM / embeddings
LLM_PROVIDER=
LLM_API_KEY=
LLM_MODEL=
EMBEDDING_MODEL=

# Frontend URL for CORS
FRONTEND_ORIGIN=http://localhost:5173
```

These names are proposed conventions; adjust them to match `settings.py` and the provider SDKs you choose.

Depending on the Google OAuth flow, you may need additional settings such as a redirect URI, OAuth scopes, and a secure token store. Do not put real access tokens, refresh tokens, or service-account JSON into the repository.

For a local setup, create a private `.env` file based on `.env.example`. Ensure `.env`, credential files, and generated company data are covered by `.gitignore`.

---

## 14. Local Development Setup

The commands below are a starting point. They assume a Python backend and a JavaScript frontend. Add the exact dependency versions and Docker/FalkorDB configuration your implementation uses.

### Prerequisites

- Git
- A supported Python version
- Node.js and npm, if using the React frontend
- Docker and Docker Compose, if running FalkorDB in containers
- Credentials and required scopes for the integrations you want to test
- An API key for the chosen LLM provider, if using a hosted model

### Step 1: Clone the repository

```bash
git clone <your-repository-url>
cd company-brain
```

### Step 2: Configure environment variables

Copy the example template to a local environment file. On macOS/Linux:

```bash
cp .env.example .env
```

If your backend uses `backend/.env`, create that file instead or configure your settings loader to read the root file. Keep the convention consistent with `settings.py`.

Fill in only the credentials for integrations you are ready to test.

### Step 3: Start FalkorDB

If Docker Compose is configured to start FalkorDB:

```bash
docker compose up -d falkordb
```

The service name `falkordb` is an example; use the name declared in your actual `docker-compose.yml`. If no service has been configured yet, add a FalkorDB service using the official image and the required persistent-volume and authentication settings.

### Step 4: Set up the Python backend

From the repository root:

```bash
python -m venv backend/.venv
```

Activate it:

**Windows PowerShell**
```powershell
.\backend\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source backend/.venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the API from the repository root:

```bash
uvicorn app.main:app --reload --app-dir backend
```

This command assumes `backend/app/main.py` exports an `app` instance and dependencies are installed. If your import/package configuration differs, adjust the command accordingly.

Open `http://127.0.0.1:8000/docs` to inspect the registered endpoints.

### Step 5: Set up the frontend

```bash
cd frontend
npm install
```

Create the frontend environment file required by your frontend toolchain, then start the development server:

```bash
npm run dev
```

The actual scripts depend on `frontend/package.json`. Configure the frontend API base URL to point to the FastAPI server.

### Step 6: Verify the basic system

Before connecting every provider, verify in this order:

1. The backend starts without import/configuration errors.
2. The health endpoint responds.
3. The backend can connect to FalkorDB.
4. A small synthetic graph can be written and queried.
5. A sample question can retrieve context and return a response.
6. Each external integration can authenticate and ingest a small authorized sample.

Do not begin by ingesting an entire workspace. Start small, verify permissions and data quality, and expand gradually.

---

## 15. Implementation Order

Build a thin, end-to-end working slice before implementing every advanced module.

### Phase 1 — Foundation

- [ ] Create the repository and folder structure.
- [ ] Add `.gitignore`, `.env.example`, and dependency manifests.
- [ ] Implement FastAPI startup, settings, logging, and health checks.
- [ ] Configure FalkorDB and verify connection/query behavior.
- [ ] Define initial graph labels, relationships, and stable IDs.

### Phase 2 — Shared ingestion model

- [ ] Define common knowledge models.
- [ ] Implement normalization and content hashing.
- [ ] Implement an idempotent graph builder and repository.
- [ ] Add tests using synthetic records.

### Phase 3 — Data integrations

- [ ] Implement GitHub API sync and selected webhooks.
- [ ] Implement Slack API sync and selected events.
- [ ] Implement Google Drive listing and Google Docs content extraction.
- [ ] Add source URLs, timestamps, and provider IDs.
- [ ] Handle pagination, retries, rate limits, and updates.

### Phase 4 — Search and RAG

- [ ] Implement graph retrieval.
- [ ] Add chunking and an embedding model.
- [ ] Implement vector retrieval using the chosen supported storage/search setup.
- [ ] Combine retrieval results and build context.
- [ ] Add LLM answer generation and source references.
- [ ] Test answers against known questions and expected evidence.

### Phase 5 — Product experience

- [ ] Implement chat, search, graph exploration, and integration status endpoints.
- [ ] Build the frontend pages.
- [ ] Add loading, empty, and error states.
- [ ] Show source citations and links in answers.
- [ ] Demonstrate cross-source reasoning using a controlled dataset.

### Phase 6 — Reliability and deployment

- [ ] Verify webhook signatures and OAuth flows.
- [ ] Enforce source permissions and user access rules.
- [ ] Add structured logs and useful health checks.
- [ ] Test duplicate events and interrupted syncs.
- [ ] Configure Docker and persistent database storage.
- [ ] Document deployment and recovery procedures.

---

## 16. Testing

Keep tests close to the behavior they validate.

Suggested coverage:

- **Integration tests:** provider parsing, pagination, webhook signature verification, and API error handling.
- **Ingestion tests:** normalization, stable IDs, deduplication, updates, and chunking.
- **Graph tests:** node/relationship creation, parameterized queries, and graph traversal.
- **RAG tests:** retrieval relevance, source attribution, insufficient-evidence behavior, and context limits.
- **Chat tests:** API validation, error handling, and response schema.
- **Frontend tests:** chat states, citations, integration status, and graph interaction.

Use mocked provider responses and synthetic content in unit tests. Keep a smaller number of integration tests that use a dedicated test graph and explicitly configured test credentials.

Example backend test command:

```bash
pytest backend/tests
```

Run it from the repository root in an environment where pytest and the project dependencies are installed. Adjust the command if your test configuration uses a different working directory.

---

## 17. Security and Privacy

Company Brain may process private messages, code metadata, and internal documents. Security and access control are core requirements, not optional polish.

- Never commit API keys, OAuth tokens, webhook secrets, private keys, or service-account credential files.
- Verify GitHub webhook signatures and Slack request signatures before accepting events.
- Use the minimum provider scopes needed for the features being implemented.
- Respect source-system permissions. Do not expose private channel messages or restricted documents to users who cannot access them.
- Keep source identity and visibility metadata with ingested content so retrieval can enforce access rules.
- Authenticate and authorize user-facing API routes before deploying to real users.
- Use TLS for deployed services and secure database credentials.
- Avoid logging full private message/document content or secrets.
- Treat retrieved text as untrusted input; it may contain prompt-injection attempts.
- Apply retention and deletion policies to stored source content and derived embeddings.
- Rotate credentials if they are accidentally exposed.
- Use synthetic or explicitly approved data for demos and tests.

A graph database does not automatically enforce the permissions of GitHub, Slack, or Google. Your application must design and implement access controls for both ingestion and retrieval.

---

## 18. Git and `.gitignore`

Keep the following tracked:

- Application source code under `backend/app/`.
- Tests and safe test fixtures.
- Frontend source code.
- `requirements.txt`, `package.json`, and lockfiles.
- Dockerfiles and shared `docker-compose.yml`.
- `.env.example` templates containing placeholders only.
- README and other project documentation.

Ignore the following:

- `.env` files containing real local credentials.
- Python virtual environments and `__pycache__/`.
- `node_modules/` and generated frontend builds.
- Local database persistence and dumps.
- Logs, caches, and temporary files.
- Raw or processed company data unless it is approved, synthetic, and intentionally versioned.
- OAuth token files and provider credential JSON.

If a secret has already been committed, adding it to `.gitignore` is not sufficient. Remove it from tracking, rotate the secret, and consider repository-history cleanup if necessary.

---

## 19. Team Responsibilities

For a two-person team, a useful initial split is:

### Developer A — Integrations and knowledge storage

- GitHub, Slack, and Google API clients.
- Parsers, mappers, and normalization.
- Ingestion pipeline and deduplication.
- FalkorDB schema, graph builder, and persistence.
- Integration and graph tests.

### Developer B — Retrieval and user experience

- Graph and vector retrieval.
- RAG pipeline and LLM prompts/client.
- Chat/search/graph API services.
- Frontend pages and components.
- Answer citations and retrieval quality tests.

### Shared ownership

Both developers should agree on the common knowledge model, graph schema, environment variable names, API contracts, error handling, and security requirements before building against them. Developer A's graph/normalization contract is the boundary that allows Developer B's retrieval work to proceed independently.

---

## 20. Troubleshooting

### Backend cannot import `app`

- Confirm the current working directory and `uvicorn` command.
- Confirm `backend/app/main.py` exists and exports `app`.
- Activate the correct virtual environment and install requirements.

### FalkorDB connection fails

- Confirm the database container/process is running.
- Check host, port, password, and graph name.
- If the backend is running inside Docker, `localhost` refers to that container, not the FalkorDB container; use the Compose service name on the shared network.
- Confirm the Python client API matches the installed FalkorDB client version.

### Provider authentication fails

- Check credentials, redirect URI, scopes, app installation, and token expiry.
- Verify webhook signatures and endpoint configuration.
- Check provider rate limits and API permissions.

### Duplicate graph entities appear

- Use stable provider IDs and deterministic internal IDs.
- Use idempotent create/update operations.
- Deduplicate webhook deliveries and ensure retries do not duplicate side effects.

### Answers have weak or missing citations

- Preserve source URLs and identifiers during parsing and normalization.
- Include source metadata in retrieval results and context.
- Require the answer formatter to return citations linked to retrieved evidence.
- Test with questions whose supporting documents are known.

### The LLM invents details

- Inspect the retrieved evidence first.
- Improve retrieval and context selection.
- Explicitly instruct the model to distinguish evidence from inference and report insufficient evidence.
- Validate citations against actual retrieved sources.

---

## 21. Contributing

1. Create a feature branch.
2. Keep provider-specific code inside its integration module.
3. Reuse the shared normalization and graph persistence layers.
4. Add or update tests for changed behavior.
5. Never commit secrets or private company data.
6. Update this README when architecture, setup commands, environment variables, or API contracts change.
7. Open a pull request with a concise summary, test results, and any configuration changes.

Suggested branch names:

```text
feature/github-ingestion
feature/slack-ingestion
feature/google-docs
feature/hybrid-rag
feature/knowledge-graph-ui
fix/webhook-validation
```

---

## 22. Roadmap

- [ ] FastAPI foundation and configuration
- [ ] FalkorDB connection and initial graph schema
- [ ] Common knowledge model and idempotent ingestion
- [ ] GitHub ingestion
- [ ] Slack ingestion
- [ ] Google Drive/Docs ingestion
- [ ] Graph search
- [ ] Chunking and embeddings
- [ ] Hybrid retrieval
- [ ] LLM answer generation with source references
- [ ] Chat interface
- [ ] Knowledge graph visualization
- [ ] Integration status and synchronization UI
- [ ] Access control, observability, and deployment hardening

Mark items complete only after implementation and testing.

---

## License

Add the project's chosen license in `LICENSE` and update this section to identify it.

---

**Company Brain — connect company knowledge, understand the relationships, and answer questions with evidence.**
