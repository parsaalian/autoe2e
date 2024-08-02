#!/bin/bash
docker run -d -it -p 9966:9966 --name=petclinic --entrypoint=/app/entrypoint.sh webappdockers/petclinic-rest:latest