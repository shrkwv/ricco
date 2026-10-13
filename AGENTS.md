# Ricco — Base44 Dev Environment

## What this is
Ricco is a **Python 3.12 CLI reconnaissance framework** managed with **uv**, with a **PHP web frontend** (from the separate `shrkwv/ricco-web` repo). The web UI lets you select a vector or strategy, enter a target, and view results in a table. The PHP backend (`assets/php/vector.php`, `assets/php/strategy.php`) calls `python ricco.py --output-json` via `shell_exec()` and returns JSON.

## Architecture
- **Single container** (`web` service) running Apache+PHP 7.4 with a uv-managed Python 3.12 runtime
- The `ricco-web` frontend files are downloaded at Docker build time into `/var/www/html/ricco-web/`
- The Ricco source (this repo) is bind-mounted at `/var/www/html/ricco-web/ricco/`
- uv installs Python 3.12 under `/opt/uv/python` and the dependency venv at `/opt/ricco/.venv` (`uv sync --frozen` at build); `python` on PATH resolves to that venv
- `docker-entrypoint.sh` fixes bind-mount permissions (chmod a+rX) so Apache's `www-data` can read the Ricco source
- Served on port 3000 (mapped to Apache's port 80)

## Running the app
```bash
docker compose -f docker-compose.base44.yml up -d --build
# Preview at http://localhost:3000
```

## Running the CLI directly
```bash
docker compose -f docker-compose.base44.yml exec -T web python /var/www/html/ricco-web/ricco/ricco.py --target google.com --vector dns_info
docker compose -f docker-compose.base44.yml exec -T web python /var/www/html/ricco-web/ricco/ricco.py --show-vectors
```

## Missing __init__.py files
The original repo was missing `__init__.py` files in `core/`, `core/base/`, `utils/`, `vectors/`, and all `vectors/*/` subdirectories. These were created as empty files so Python can import packages. Do not delete them.

## External credentials (optional)
Some vectors need API keys configured in `core/ricco.ini`:
- **Flickr** (`flickr_by_radius`) — Flickr API key
- **Google** (`location_info`) — Google API key

Core vectors (`dns_info`, `dns_zone_transfer`, `http_grab_banner`, `iana_whois_info`, `domain_whois_info`, `ip_whois_info`, `subdomains_fuzzing`, `dirs_fuzzing`, `suffixes_fuzzing`, `mails_on_host`) work without any credentials.

## Dependencies
- Python 3.12 (installed by uv in the image; no apt python)
- Dependencies in `pyproject.toml`, locked in `uv.lock`: dnspython 2.x, ipwhois, lxml, xmltodict
- PHP 7.4 + Apache 2.4 (from `php:7.4-apache` base image)
- `nmap` is needed for the `nmap_banner` vector (not installed in the image)

## Dropped in the Python 3 port
Dead code and dead services were removed instead of ported: `add-ons/`, `vectors/infogather/old/`, the Panoramio / YouTube gdata / old-OAuth Instagram vectors, the unregistered `cord_to_address` duplicate, `utils/site2list.py`, `utils/json2html.py`, and the `core/base/test_props.py` scratch file.
