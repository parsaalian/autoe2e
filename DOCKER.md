# Docker Setup Guide

This guide explains how to run AutoE2E using Docker Compose. All services (backend, frontend, and main script) are containerized and orchestrated together.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Services](#services)
- [Helper Scripts](#helper-scripts)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker and Docker Compose installed
- A `.env` file with required API keys (see [Environment Variables](#environment-variables))

## Quick Start
   ```bash
   cd autoe2e
   docker-compose up --build
   # To shut down
   docker-compose down
   ```

   To run it after the first time, simply run docker-compose up, without the build.

### First Time Setup

1. **Navigate to the autoe2e directory(The project file, not /autoe2e/autoe2e):**
   ```bash
   cd autoe2e
   ```

2. **Create your `.env` file:**
   ```bash
   # Create .env file in the autoe2e directory
   cat > .env << EOF
   APP_NAME=PETCLINIC
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ATLAS_URI=your_mongodb_atlas_uri_here
   EOF
   ```
   
   Or manually create `autoe2e/.env` with:
   ```env
   APP_NAME=PETCLINIC
   ANTHROPIC_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-proj-...
   ATLAS_URI=mongodb+srv://...
   ```

3. **Start everything:**
   ```bash
   docker-compose up --build
   ```

### Daily Usage

**Start services:**
```bash
cd autoe2e
docker-compose up
```

**Start in background:**
```bash
docker-compose up -d
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f main
docker-compose logs -f frontend
docker-compose logs -f backend
```

**Stop services:**
```bash
docker-compose down
```

## Environment Variables

Create a `.env` file in the `autoe2e` directory with the following variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `APP_NAME` | Application name (must match a config in `./configs`) | Yes |
| `ANTHROPIC_API_KEY` | API key for Anthropic (LLM calls) | Yes |
| `OPENAI_API_KEY` | API key for OpenAI (embeddings) | Yes |
| `ATLAS_URI` | MongoDB Atlas URI for database | Yes |

**Important formatting rules:**
- No quotes around values
- No spaces around the `=` sign
- No trailing whitespace
- File must be in `autoe2e/` directory (same as `docker-compose.yml`)

Example:
```env
APP_NAME=PETCLINIC
ANTHROPIC_API_KEY=sk-ant-abc123...
OPENAI_API_KEY=sk-proj-xyz789...
ATLAS_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname
```

## Services

The Docker Compose setup includes three services:

1. **backend** - PetClinic REST API
   - Image: `webappdockers/petclinic-rest:latest`
   - Port: `9966`
   - Health check: Waits for API to respond

2. **frontend** - Angular frontend application
   - Built from: `Dockerfile.frontend`
   - Port: `4200`
   - First compile: Takes 2-3 minutes
   - Uses `--legacy-peer-deps` for dependency installation

3. **main** - Python script for E2E test generation
   - Built from: `Dockerfile.main`
   - Runs: `main.py` automatically
   - Uses: Python 3.11, Chrome/ChromeDriver for Selenium
   - Network: Host mode (to access `localhost:4200`)

### Startup Order

1. Backend starts and waits until healthy
2. Frontend starts after backend is healthy
3. Main script starts after both services are running

## Helper Scripts

All helper scripts are located in the `scripts/` directory. Run them from the `autoe2e/` directory:

### `scripts/verify-env.sh`
**Purpose:** Verify `.env` file exists and contains required variables

**Usage:**
```bash
chmod +x scripts/verify-env.sh
./scripts/verify-env.sh
```

**What it does:**
- Checks if `.env` file exists
- Verifies all required variables are present
- Shows first few characters of keys (for verification)
- Checks Docker Compose configuration

---

### `scripts/clean.sh`
**Purpose:** Clean up containers and images for a fresh rebuild

**Usage:**
```bash
chmod +x scripts/clean.sh
./scripts/clean.sh
docker-compose up --build
```

**What it does:**
- Stops all containers
- Removes containers
- Removes project images
- Prunes dangling images

---

### `scripts/clean-all.sh`
**Purpose:** Nuclear cleanup - removes everything (containers, images, volumes)

**Usage:**
```bash
chmod +x scripts/clean-all.sh
./scripts/clean-all.sh
docker-compose build --no-cache
docker-compose up
```

**What it does:**
- Stops and removes all containers
- Removes all project images
- Removes volumes
- Prunes Docker system

**Use when:** Containers are stuck, images are corrupted, or you need a completely fresh start

---

### `scripts/test-openai-key.sh`
**Purpose:** Test if OpenAI API key is valid from inside the container

**Usage:**
```bash
chmod +x scripts/test-openai-key.sh
./scripts/test-openai-key.sh
```

**What it does:**
- Checks if key is loaded in container
- Validates key format
- Tests API connection
- Reports if key is valid or invalid

---

### `scripts/check-frontend.sh`
**Purpose:** Debug frontend container issues

**Usage:**
```bash
chmod +x scripts/check-frontend.sh
./scripts/check-frontend.sh
```

**What it does:**
- Lists frontend containers
- Shows recent logs
- Checks if `ng serve` is running

## Troubleshooting

### Environment Variables Not Loading

**Symptoms:** API key errors, variables not found

**Solutions:**
1. Verify `.env` file is in `autoe2e/` directory (same as `docker-compose.yml`)
2. Check file format (no quotes, no spaces around `=`)
3. Run `./scripts/verify-env.sh` to diagnose
4. Restart containers: `docker-compose down && docker-compose up`

### Frontend Container Unhealthy

**Symptoms:** Frontend marked as unhealthy, services won't start

**Solutions:**
1. Check frontend logs: `docker-compose logs frontend`
2. Wait longer - Angular takes 2-3 minutes to compile on first run
3. Run `./scripts/check-frontend.sh` to debug
4. Clean and rebuild: `./scripts/clean.sh && docker-compose up --build`

### Backend Container Unhealthy

**Symptoms:** Backend healthcheck fails, frontend won't start

**Solutions:**
1. Check backend logs: `docker-compose logs backend`
2. Verify port 9966 is not in use
3. Wait - backend takes ~1 minute to start
4. Check healthcheck: `curl http://localhost:9966/petclinic/api/owners`

### Main Script Can't Connect to Frontend

**Symptoms:** Connection refused errors, Selenium can't access localhost:4200

**Solutions:**
1. Verify frontend is running: `docker-compose ps`
2. Check frontend is accessible: `curl http://localhost:4200`
3. Ensure main container uses host networking (already configured)
4. Check frontend logs for compilation errors

### Chrome/Selenium Issues

**Symptoms:** Chrome errors, headless mode not working

**Solutions:**
1. Chrome automatically runs in headless mode in Docker
2. Check main container logs: `docker-compose logs main`
3. Verify Chrome is installed: `docker-compose exec main which google-chrome-stable`

### Containers Stuck or Cached

**Symptoms:** Old containers, changes not taking effect

**Solutions:**
1. Clean and rebuild: `./scripts/clean.sh && docker-compose up --build`
2. Nuclear cleanup: `./scripts/clean-all.sh && docker-compose build --no-cache && docker-compose up`

## Volumes

The following directories are mounted as volumes:

- `./configs` → `/app/configs` (read-only) - Configuration files
- `./tmp` → `/app/tmp` (read-write) - Temporary files and screenshots
- `./report` → `/app/report` (read-write) - Generated reports

## Architecture Notes

- **Frontend:** Uses `--legacy-peer-deps` flag for npm install to handle dependency conflicts
- **Chrome:** Automatically runs in headless mode when detected in Docker (via `/.dockerenv` check)
- **Network:** Main service uses `network_mode: host` so Selenium can access `localhost:4200`
- **Health Checks:** Backend has healthcheck; frontend does not (to allow time for Angular compilation)

## Additional Resources

- Main README: `README.md`
- Docker Compose file: `docker-compose.yml`
- Frontend Dockerfile: `Dockerfile.frontend`
- Main Dockerfile: `Dockerfile.main`

