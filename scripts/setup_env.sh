#!/bin/bash
# Quick environment setup script

echo "🚀 RAG Pipeline Environment Setup"
echo "================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

if ! python -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
    echo "⚠️  Warning: Python 3.11+ recommended (you have $PYTHON_VERSION)"
fi

echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating .env from template..."
        cp .env.example .env
        echo "✅ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
        echo "   - OPENAI_API_KEY"
        echo "   - CO_API_KEY"
    else
        echo "⚠️  .env.example not found. Creating basic .env..."
        cat > .env << EOF
# OpenAI API Key (required)
OPENAI_API_KEY=your-openai-api-key-here

# Cohere API Key (required for re-ranking)
CO_API_KEY=your-cohere-api-key-here
EOF
        echo "✅ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and add your actual API keys"
    fi
else
    echo "✅ .env file already exists"
fi

echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys (if you haven't already)"
echo "  2. Index sample documents:"
echo "     python main.py add -p 'sample_data/source/'"
echo "  3. Try a query:"
echo "     python main.py query 'What year was AuraTech founded?'"
echo "  4. Or start the web interface:"
echo "     reflex run"
echo ""





