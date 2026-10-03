# Worker Application (`apps/worker`)

**Purpose:** Asynchronous queue worker and scheduler powered by Arq and Redis Streams. Handles long-running agent flows, scheduled posts, and signal polling.

## Files
- `__init__.py` — Package entrypoint.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`

<!-- END GENERATED -->

## Running Locally
```bash
uv run arq apps.worker.main.WorkerSettings
```
