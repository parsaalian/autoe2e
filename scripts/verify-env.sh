#!/bin/bash
# Verify .env file is readable and check docker-compose config

echo "=== Checking .env file ==="
if [ -f .env ]; then
    echo "✅ .env file exists"
    echo ""
    echo "Checking for required variables:"
    grep -q "OPENAI_API_KEY" .env && echo "✅ OPENAI_API_KEY found" || echo "❌ OPENAI_API_KEY NOT FOUND"
    grep -q "ANTHROPIC_API_KEY" .env && echo "✅ ANTHROPIC_API_KEY found" || echo "❌ ANTHROPIC_API_KEY NOT FOUND"
    grep -q "ATLAS_URI" .env && echo "✅ ATLAS_URI found" || echo "❌ ATLAS_URI NOT FOUND"
    echo ""
    echo "First few characters of keys (for verification):"
    grep "OPENAI_API_KEY" .env | head -1 | sed 's/\(.\{15\}\).*/\1.../'
    grep "ANTHROPIC_API_KEY" .env | head -1 | sed 's/\(.\{15\}\).*/\1.../'
else
    echo "❌ .env file NOT FOUND in current directory"
    echo "Current directory: $(pwd)"
    echo "Looking for: $(pwd)/.env"
fi

echo ""
echo "=== Checking docker-compose config ==="
docker-compose config 2>&1 | grep -A 2 "OPENAI_API_KEY" || echo "OPENAI_API_KEY not found in docker-compose config"

