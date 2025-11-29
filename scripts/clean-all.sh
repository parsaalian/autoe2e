#!/bin/bash
# Nuclear cleanup - removes everything related to this project

echo "=== Stopping all containers ==="
docker-compose down

echo "=== Removing ALL containers ==="
docker-compose rm -f
docker ps -a --filter "name=frontend" --format "{{.ID}}" | xargs -r docker rm -f
docker ps -a --filter "name=petclinic" --format "{{.ID}}" | xargs -r docker rm -f

echo "=== Removing all images ==="
docker rmi autoe2e_frontend autoe2e_main 2>/dev/null || true

echo "=== Removing volumes ==="
docker-compose down -v

echo "=== Pruning Docker system ==="
docker system prune -f

echo ""
echo "✅ Complete cleanup done! Run 'docker-compose build --no-cache && docker-compose up' to rebuild from scratch."

