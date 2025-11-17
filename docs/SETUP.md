# Setup Guide

Complete installation and configuration guide for the RAG Pipeline project.

---

## Prerequisites

- **Python 3.13+** (3.11+ should work)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Cohere API Key** ([Get one here](https://cohere.com/))
- **Git** (for cloning the repository)

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd simple-rag-pipeline
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **Reflex** - Web framework
- **LanceDB** - Vector database
- **OpenAI** - LLM API
- **Cohere** - Re-ranking API
- **Docling** - Document processing
- **SQLAlchemy** - Database ORM
- And other dependencies

### 4. Set Up Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit .env with your actual API keys
nano .env  # or use your favorite editor
```

Your `.env` file should look like:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
CO_API_KEY=xxxxxxxxxxxxx
```

**Important:** Never commit your `.env` file to Git! It's already in `.gitignore`.

---

## Initial Setup

### 1. Initialize the Database

The Reflex app uses SQLite for storing chat history and evaluations.

```bash
# Initialize Alembic migrations (if needed)
alembic upgrade head
```

### 2. Index Sample Documents

Before using the system, you need to index some documents:

```bash
# Reset the vector database (optional, only if you want a clean start)
python main.py reset

# Index the sample documents
python main.py add -p "sample_data/source/"
```

This will:
- Parse the PDF files
- Split them into chunks
- Generate embeddings
- Store them in LanceDB

You should see output like:
```
🔍 Adding documents: sample_data/source/auratechdynamics_history.pdf, ...
✅ Indexed 63 chunks
```

---

## Usage

### Command Line Interface (CLI)

The CLI provides several commands:

#### Query Documents
```bash
python main.py query "What year was AuraTech Dynamics founded?"
```

#### Add New Documents
```bash
# Add a single file
python main.py add -p "path/to/document.pdf"

# Add all files in a directory
python main.py add -p "path/to/directory/"
```

#### Evaluate the System
```bash
python main.py evaluate -f "sample_data/eval/sample_questions.json"
```

This runs all test questions and shows:
- Generated answers vs. expected answers
- Precision, Recall, MRR metrics
- Correctness evaluation

#### Run Full Pipeline
```bash
# Reset DB, add documents, and evaluate
python main.py run
```

### Web Interface (Reflex)

The web interface provides an evaluation dashboard where you can:
- Select test questions from a dropdown
- View generated vs. expected answers
- See detailed retrieval metrics (Precision, Recall, MRR)
- Analyze AI reasoning for correctness

#### Start the Web App

```bash
# Make sure you've indexed documents first
python main.py add -p "sample_data/source/"

# Start Reflex
reflex run
```

The app will be available at:
- **Frontend:** http://localhost:3000 (or 3001 if 3000 is busy)
- **Backend API:** http://localhost:8000 (or 8001 if 8000 is busy)

#### First-Time Setup

On first run, Reflex will:
1. Install Node.js dependencies (takes a few minutes)
2. Build the frontend
3. Start both frontend and backend servers

Subsequent runs are much faster.

---

## Troubleshooting

### Environment Variable Issues

**Problem:** `OpenAI API key not found` or similar errors

**Solution:**
1. Check your `.env` file exists in the project root
2. Verify it contains the correct keys (no spaces around `=`)
3. Make sure you activated the virtual environment

Test if environment variables are loaded:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv('.env'); print('OpenAI Key:', os.getenv('OPENAI_API_KEY')[:20] + '...' if os.getenv('OPENAI_API_KEY') else 'NOT FOUND')"
```

### Database Issues

**Problem:** Database errors or migration issues

**Solution:**
```bash
# Reset the Reflex database
rm rag_chat.db

# Run migrations again
alembic upgrade head
```

### LanceDB Issues

**Problem:** Vector database errors or no results found

**Solution:**
```bash
# Delete the vector database and re-index
rm -rf data/sample-lancedb/

# Re-index documents
python main.py add -p "sample_data/source/"
```

### Port Already in Use

**Problem:** `Address already in use` when starting Reflex

**Solution:** Reflex automatically detects busy ports and uses alternatives (3001, 8001, etc.). Just use the port shown in the terminal output.

Or manually kill the process:
```bash
# Find what's using the port
lsof -i :3000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>
```

### Import Errors

**Problem:** `ModuleNotFoundError` or import issues

**Solution:**
1. Make sure you're in the project root directory
2. Activate the virtual environment: `source venv/bin/activate`
3. Reinstall dependencies: `pip install -r requirements.txt`

### Reflex Won't Start

**Problem:** Reflex initialization fails

**Solution:**
```bash
# Clean Reflex cache
rm -rf .web .states

# Reinstall frontend dependencies
reflex init
```

---

## Advanced Configuration

### Custom Document Sources

To use your own documents:

1. Place PDF files in a directory (e.g., `my_documents/`)
2. Index them:
   ```bash
   python main.py reset  # Optional: clear existing data
   python main.py add -p "my_documents/"
   ```

### Custom Evaluation Questions

Create a JSON file with your test questions:

```json
[
  {
    "question": "What is X?",
    "expected_answer": "X is...",
    "relevant_doc_ids": ["doc1.pdf:0", "doc1.pdf:5"]
  }
]
```

Run evaluation:
```bash
python main.py evaluate -f "path/to/questions.json"
```

### Reflex Configuration

Edit `rxconfig.py` to customize:
- Database URL
- API URLs
- Frontend/backend ports

---

## Development Mode

To run in development mode with hot reloading:

```bash
reflex run --env dev
```

Changes to Python files will automatically reload the backend.
Changes to frontend components require a manual refresh.

---

## Production Deployment

To build for production:

```bash
# Export static build
reflex export

# The build will be in .web/_static/
```

For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Setting up proper authentication
- Using environment-specific `.env` files
- Deploying with Docker

---

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- Try the sample questions in the web interface
- Add your own documents and questions
- Explore the source code in `src/` and `rag_chat_app/`

---

## Getting Help

- Check the [main README](../README.md)
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Open an issue on GitHub (if applicable)

---

**Enjoy building with RAG! 🚀**





