## 2.15.1-r1 (2026-06-16)

### Changed

- **Nginx Proxy Manager**: updated to v2.15.1
- **Base image**: updated to `ghcr.io/hassio-addons/base:21.0.0` (Alpine 3.24)
- **Python patcher**: replaced 48 fragile sed commands with a Python script (`scripts/patch-npm.py`) — 9 patches, self-validating
- **node_modules cleanup**: replaced unmaintained `modclean` with `npx clean-modules`

## 2.14.0-r1 (2026-04-18)

### Changed

- **Base image**: updated to `ghcr.io/hassio-addons/base:20.0.4` (GitHub Actions)
- **Nginx Proxy Manager**: updated to v2.14.0
- **Patch organization**: kept inline in Dockerfile for simplicity

### Notes

- Compatible with Home Assistant OS 17.2, Home Assistant Core 2026.4.3 (aarch64)
- DuckDNS certificates issuance confirmed working
