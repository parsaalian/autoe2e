#!/bin/bash
# Check frontend container status and logs

echo "=== Checking frontend container ==="
docker ps -a | grep frontend

echo ""
echo "=== Latest frontend container logs ==="
CONTAINER_ID=$(docker ps -a | grep frontend | head -1 | awk '{print $1}')
if [ ! -z "$CONTAINER_ID" ]; then
    echo "Container ID: $CONTAINER_ID"
    docker logs $CONTAINER_ID 2>&1 | tail -100
else
    echo "No frontend container found"
fi

echo ""
echo "=== Checking if ng serve is running ==="
if [ ! -z "$CONTAINER_ID" ]; then
    docker exec $CONTAINER_ID ps aux 2>/dev/null | grep -i "ng serve" || echo "Cannot exec into container or ng serve not running"
fi

