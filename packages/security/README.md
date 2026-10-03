# Security Package (`packages/security`)

**Purpose:** Enforces network egress controls (SSRF protection), token encryption via AWS KMS, authentication validation, and prompt injection defenses.

## Files
- `egress.py` — `validate_egress_url` function preventing SSRF to cloud metadata and private networks.

## Public Functions & Classes
- `validate_egress_url(url: str) -> None`: Validates external target URL before requests.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `egress.py` (1 public symbols)
  - `validate_egress_url`: Validate that target URL does not resolve to private, loopback, or metadata addresses.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/security
```
