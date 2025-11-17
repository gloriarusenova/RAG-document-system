# System Architecture

This document explains the architecture and design of the RAG Pipeline system.

---

## Overview

The RAG (Retrieval Augmented Generation) Pipeline is designed with a modular architecture that separates concerns and allows for easy extension and customization.

```
┌─────────────────────────────────────────────────────────────┐
│                         User Layer                          │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (main.py)     │   Web Interface (Reflex)     │
│  - Query documents           │   - Evaluation dashboard     │
│  - Index documents           │   - Test questions          │
│  - Run evaluations           │   - Metrics visualization    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline Core                         │
│                  (src/rag_pipeline.py)                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   Indexer    │      │  Retriever   │     │  Response    │
│              │      │              │     │  Generator   │
│  Document    │      │  Vector      │     │              │
│  Processing  │      │  Search      │     │  OpenAI API  │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │
        ▼                     ▼
┌─────────────────────────────────────────┐
│          Datastore (LanceDB)            │
│                                         │
│  - Vector embeddings                    │
│  - Document chunks                      │
│  - Metadata                             │
└─────────────────────────────────────────┘
                              
                              ▼
┌─────────────────────────────────────────┐
│           Evaluator                     │
│                                         │
│  - Compare answers                      │
│  - Calculate metrics                    │
│  - AI-powered evaluation                │
└─────────────────────────────────────────┘
```

---

## Core Components

### 1. RAG Pipeline (`src/rag_pipeline.py`)

The main orchestrator that coordinates all components.

**Key Methods:**
- `reset()` - Clear the vector database
- `add_documents()` - Index new documents
- `process_query()` - Query and generate response
- `evaluate()` - Run evaluation on test questions

**Responsibilities:**
- Component initialization
- Workflow coordination
- Error handling

### 2. Datastore (`src/impl/datastore.py`)

Manages vector embeddings and document storage using LanceDB.

**Key Features:**
- Vector similarity search
- Metadata filtering
- Chunk storage and retrieval
- Embedding generation (via OpenAI)

**Technology:** LanceDB (columnar vector database)

**Storage Format:**
```python
{
    "chunk_id": "document.pdf:0",
    "content": "The document text...",
    "source": "document.pdf",
    "vector": [0.123, 0.456, ...]  # 1536-dim embedding
}
```

### 3. Indexer (`src/impl/indexer.py`)

Processes documents and creates searchable chunks.

**Process:**
1. Parse PDF using Docling
2. Split into semantic chunks
3. Extract metadata
4. Generate embeddings
5. Store in LanceDB

**Chunking Strategy:**
- Semantic chunking (preserves meaning)
- Configurable chunk size
- Overlap between chunks

### 4. Retriever (`src/impl/retriever.py`)

Searches for relevant document chunks given a query.

**Two-Stage Retrieval:**

1. **Vector Search (LanceDB)**
   - Convert query to embedding
   - Find top-N similar chunks
   - Uses L2 distance

2. **Re-ranking (Cohere)**
   - Semantic re-ranking of results
   - Improves relevance ordering
   - Reduces false positives

**Output:** Top-K most relevant chunks with similarity scores

### 5. Response Generator (`src/impl/response_generator.py`)

Generates natural language responses using OpenAI's GPT models.

**Process:**
1. Receive query + retrieved chunks
2. Construct prompt with context
3. Call OpenAI API
4. Return generated answer

**Prompt Engineering:**
- Context-aware prompts
- Clear instructions
- Citation requirements

### 6. Evaluator (`src/impl/evaluator.py`)

Evaluates system performance using test questions.

**Evaluation Metrics:**

1. **Precision**
   ```
   Precision = |Retrieved ∩ Relevant| / |Retrieved|
   ```
   "Of what I found, how much was useful?"

2. **Recall**
   ```
   Recall = |Retrieved ∩ Relevant| / |Relevant|
   ```
   "Of what I should find, how much did I find?"

3. **MRR (Mean Reciprocal Rank)**
   ```
   MRR = 1 / rank_of_first_relevant_doc
   ```
   "How quickly did I find something useful?"

**AI-Powered Correctness:**
- Compares generated vs. expected answer
- Provides reasoning for judgment
- Uses GPT-4 for evaluation

---

## Interface Layer

All core components implement abstract base classes for flexibility:

```python
src/interface/
├── base_datastore.py          # Datastore contract
├── base_indexer.py            # Indexer contract
├── base_retriever.py          # Retriever contract
├── base_response_generator.py # Generator contract
└── base_evaluator.py          # Evaluator contract
```

**Benefits:**
- Easy to swap implementations
- Consistent API across components
- Testable and mockable
- Type hints for better IDE support

---

## Web Interface Architecture

### Reflex Application (`rag_chat_app/`)

Built with [Reflex](https://reflex.dev/), a Python-based web framework.

```
rag_chat_app/
├── rag_chat_app.py          # Main app & routing
├── eval_state.py            # State management
├── models.py                # Database models (SQLite)
├── rag_service.py           # RAG pipeline integration
└── components/              # UI components
    ├── question_selector.py  # Dropdown + suggestions
    ├── eval_results.py       # Results display
    ├── metrics_display.py    # Metrics visualization
    └── chunks_display.py     # Retrieved chunks view
```

### State Management

Reflex uses reactive state:

```python
class EvalState(rx.State):
    # State variables
    all_questions: List[TestQuestion]
    selected_question: str
    evaluation_result: EvaluationResult
    
    # Event handlers
    def select_question(self, question: str):
        # Update state
        
    def evaluate_question(self):
        # Trigger evaluation
```

**State Flow:**
1. User selects question → State updates
2. User clicks "Evaluate" → Event handler triggered
3. Handler calls RAG service → Results returned
4. State updates → UI re-renders automatically

### Database Models

SQLite database for chat history:

```python
class ChatMessage(rx.Model):
    session_id: str
    question: str
    answer: str
    sources: str  # JSON
    timestamp: datetime
    avg_score: float
    num_sources: int
```

Managed by SQLAlchemy + Alembic migrations.

---

## Data Flow

### 1. Document Indexing Flow

```
PDF Document
    │
    ▼
[Docling Parser]
    │
    ▼
Text + Structure
    │
    ▼
[Chunking Algorithm]
    │
    ▼
Document Chunks
    │
    ▼
[OpenAI Embeddings API]
    │
    ▼
Vector Embeddings (1536-dim)
    │
    ▼
[LanceDB Storage]
```

### 2. Query Flow

```
User Question
    │
    ▼
[OpenAI Embeddings API]
    │
    ▼
Query Vector
    │
    ▼
[LanceDB Vector Search] → Top 20 chunks
    │
    ▼
[Cohere Re-ranking] → Top 5 chunks
    │
    ▼
[Response Generator + OpenAI API]
    │
    ▼
Generated Answer + Sources
```

### 3. Evaluation Flow

```
Test Question + Expected Answer + Relevant Doc IDs
    │
    ▼
[RAG Pipeline] → Generated Answer + Retrieved Chunks
    │
    ▼
[Metrics Calculator]
    ├─ Precision (overlap analysis)
    ├─ Recall (coverage analysis)
    └─ MRR (ranking analysis)
    │
    ▼
[AI Evaluator] → Correctness + Reasoning
    │
    ▼
Complete Evaluation Result
```

---

## Technology Stack

### Backend
- **Python 3.13** - Core language
- **LanceDB** - Vector database
- **OpenAI API** - Embeddings + LLM
- **Cohere API** - Re-ranking
- **Docling** - PDF parsing
- **SQLAlchemy** - Database ORM
- **Alembic** - Database migrations

### Frontend
- **Reflex** - Python web framework
- **React** - UI rendering (via Reflex)
- **Chakra UI** - Component library (via Reflex)

### Storage
- **LanceDB** - Vector embeddings (columnar format)
- **SQLite** - Chat history and sessions

---

## File Structure

```
simple-rag-pipeline/
│
├── src/                          # RAG pipeline core
│   ├── rag_pipeline.py           # Main orchestrator
│   │
│   ├── interface/                # Abstract base classes
│   │   ├── base_datastore.py
│   │   ├── base_indexer.py
│   │   ├── base_retriever.py
│   │   ├── base_response_generator.py
│   │   └── base_evaluator.py
│   │
│   ├── impl/                     # Concrete implementations
│   │   ├── datastore.py          # LanceDB implementation
│   │   ├── indexer.py            # Docling-based indexer
│   │   ├── retriever.py          # Vector + re-ranking retrieval
│   │   ├── response_generator.py # OpenAI response generation
│   │   └── evaluator.py          # Metrics + AI evaluation
│   │
│   └── util/                     # Helper utilities
│       ├── extract_xml.py        # XML parsing
│       ├── invoke_ai.py          # OpenAI API wrapper
│       └── metrics_calculator.py # Precision/Recall/MRR
│
├── rag_chat_app/                 # Reflex web interface
│   ├── rag_chat_app.py           # Main Reflex app
│   ├── eval_state.py             # State management
│   ├── models.py                 # SQLite models
│   ├── rag_service.py            # RAG integration
│   └── components/               # UI components
│
├── sample_data/                  # Test data
│   ├── source/                   # Sample PDFs
│   └── eval/                     # Test questions
│
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── main.py                       # CLI entry point
├── create_parser.py              # CLI argument parser
└── rxconfig.py                   # Reflex configuration
```

---

## Design Principles

### 1. Separation of Concerns
Each component has a single, well-defined responsibility.

### 2. Interface-Based Design
Abstract base classes define contracts, implementations can vary.

### 3. Modularity
Components can be swapped or extended without affecting others.

### 4. Testability
Pure functions and clear interfaces make testing easier.

### 5. Configuration Over Code
Settings are externalized (environment variables, config files).

---

## Extension Points

### Add New Document Types
Implement a new `BaseIndexer` for different file formats (Word, HTML, etc.)

### Use Different Vector Database
Implement `BaseDatastore` for Pinecone, Weaviate, or Chroma

### Swap LLM Provider
Implement `BaseResponseGenerator` for Claude, Gemini, or local models

### Custom Retrieval Strategy
Implement `BaseRetriever` with different ranking algorithms

### Enhanced Evaluation
Extend `BaseEvaluator` with custom metrics or evaluation criteria

---

## Performance Considerations

### Indexing Performance
- **Batch processing** - Index multiple documents together
- **Async operations** - Parallelize embedding generation
- **Chunk size** - Balance between granularity and performance

### Query Performance
- **Vector search** - LanceDB is optimized for fast similarity search
- **Re-ranking** - Only re-rank top-K results (not all chunks)
- **Caching** - Cache embeddings for repeated queries

### Scalability
- **LanceDB** - Columnar storage scales to millions of vectors
- **Reflex** - Can deploy with multiple workers
- **Database** - SQLite sufficient for demos; use PostgreSQL for production

---

## Security Considerations

### API Keys
- Never commit `.env` files
- Use environment variables
- Rotate keys regularly

### Data Privacy
- Local vector database (no data sent except to OpenAI/Cohere)
- User data stored locally in SQLite
- No external telemetry by default

### Input Validation
- Sanitize user queries
- Validate file uploads
- Rate limiting for API calls

---

## Future Enhancements

### Planned Features
- [ ] Multi-user authentication
- [ ] Document management UI
- [ ] Batch evaluation reports
- [ ] Advanced metrics visualization
- [ ] Custom prompt templates
- [ ] Document upload via web interface
- [ ] Export evaluation results (CSV/JSON)

### Experimental
- [ ] Multi-modal support (images, tables)
- [ ] Conversation context tracking
- [ ] Fine-tuned embedding models
- [ ] Hybrid search (keyword + vector)

---

## Related Documentation

- [Setup Guide](SETUP.md) - Installation and configuration
- [Main README](../README.md) - Project overview
- [Cleanup Recommendations](../CLEANUP_RECOMMENDATIONS.md) - Project cleanup guide

---

**Questions?** Open an issue or check the source code comments for implementation details.





