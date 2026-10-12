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


