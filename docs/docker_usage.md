# Docker Workflow

## Build Containers
- From repo root: `docker compose build`
- Builds two images:
  - `pipeline`: Python 3.11 environment with dependencies from `requirements.txt`
  - `frontend`: Node 20/Vite dev server for `tag-governance-app`

## Start Services
- Dev stack (detached): `docker compose up -d`
- Tail logs: `docker compose logs -f`
- Stop everything: `docker compose down`

## Work in the Python Container
- Open shell: `docker compose exec pipeline bash`
- Run pipeline script: `docker compose exec pipeline python scripts/run_pipeline.py --config configs/pipeline_v2.yaml`
- Container mounts the repo at `/workspace`

## React Frontend
- Local dev server exposed on http://localhost:5173 after `docker compose up`
- Hot reload works because `./tag-governance-app` is bind-mounted into the container

## Additional Notes
- `pipeline` service idles (`tail -f /dev/null`) until you attach and run commands
- Rebuild after dependency changes: `docker compose build --no-cache`
