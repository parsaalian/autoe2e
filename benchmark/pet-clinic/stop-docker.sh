#!/bin/bash
cov="${1:-coverage}"
docker exec petclinic /app/exitScript.sh
docker cp petclinic:/jacoco/cov $cov
docker stop petclinic
docker rm petclinic
