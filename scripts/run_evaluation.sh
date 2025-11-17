#!/bin/bash
# Run RAG pipeline evaluation with sample questions

# Exit on error
set -e

echo "🔍 RAG Pipeline Evaluation"
echo "================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Activating venv..."
    
    # Try to activate from common locations
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "../venv/bin/activate" ]; then
        source ../venv/bin/activate
    else
        echo "❌ Could not find venv. Please activate manually."
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Please create .env from .env.example and add your API keys."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set in .env"
    exit 1
fi

if [ -z "$CO_API_KEY" ]; then
    echo "❌ CO_API_KEY not set in .env"
    exit 1
fi

echo "✅ Environment variables loaded"
echo "✅ API keys configured"
echo ""

# Run evaluation
echo "Running evaluation..."
python main.py evaluate

echo ""
echo "✅ Evaluation complete!"





