#!/bin/bash
# Clean up Docker containers and images for a fresh rebuild

echo "=== Stopping all containers ==="
docker-compose down

echo "=== Removing containers ==="
docker-compose rm -f

echo "=== Removing images ==="
docker rmi autoe2e_frontend autoe2e_main 2>/dev/null || true

echo "=== Removing dangling images ==="
docker image prune -f

echo ""
echo "✅ Cleanup complete! Run 'docker-compose up --build' to rebuild."

