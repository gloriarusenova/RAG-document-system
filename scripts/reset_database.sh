#!/bin/bash
# Reset all databases (vector DB and SQLite)

echo "⚠️  Database Reset"
echo "================================"
echo "This will delete:"
echo "  - Vector database (LanceDB)"
echo "  - Chat history (SQLite)"
echo "  - Reflex state"
echo ""
read -p "Are you sure? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

echo ""
echo "🗑️  Removing databases..."

# Remove LanceDB vector database
if [ -d "data/sample-lancedb" ]; then
    rm -rf data/sample-lancedb/
    echo "✅ Removed vector database"
else
    echo "ℹ️  No vector database found"
fi

# Remove SQLite database
if [ -f "rag_chat.db" ]; then
    rm rag_chat.db
    echo "✅ Removed chat history database"
else
    echo "ℹ️  No chat database found"
fi

# Remove Reflex state
if [ -d ".states" ]; then
    rm -rf .states/
    echo "✅ Removed Reflex state"
fi

echo ""
echo "✅ Database reset complete!"
echo ""
echo "Next steps:"
echo "  1. Index documents: python main.py add -p 'sample_data/source/'"
echo "  2. Run Reflex: reflex run"





