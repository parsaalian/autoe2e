#!/bin/bash
# Test OpenAI API key from inside the container

echo "=== Testing OpenAI API key from container ==="
docker-compose exec main python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
if key:
    print(f'Key found: {key[:10]}...{key[-4:]}')
    print(f'Key length: {len(key)}')
    print(f'Key starts with sk-: {key.startswith(\"sk-\")}')
    
    # Test the key
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        models = client.models.list()
        print('✅ API key is VALID - Successfully connected to OpenAI')
    except Exception as e:
        print(f'❌ API key is INVALID: {e}')
else:
    print('❌ OPENAI_API_KEY not found in environment')
"

