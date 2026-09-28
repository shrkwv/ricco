# Ricco — Base44 Dev Environment

## What this is
Ricco is a **Python 2.7 CLI reconnaissance framework**, not a web application. It has no web server or UI — it runs from the terminal via `python ricco.py`. The Base44 preview (port 3000) has nothing to display; the tool is exercised via `docker compose exec`.

## Running the tool
```bash
# Start the container
docker compose -f docker-compose.base44.yml up -d

# Install dependencies (first time only)
docker compose -f docker-compose.base44.yml exec -T ricco pip install -r requirements.txt

# Run a vector
docker compose -f docker-compose.base44.yml exec -T ricco python ricco.py --target google.com --vector dns_info

# Show all vectors
docker compose -f docker-compose.base44.yml exec -T ricco python ricco.py --show-vectors

# Show all strategies
docker compose -f docker-compose.base44.yml exec -T ricco python ricco.py --show-strategies

# JSON output
docker compose -f docker-compose.base44.yml exec -T ricco python ricco.py --target google.com --vector dns_info --output-json
```

## Missing __init__.py files
The original repo was missing `__init__.py` files in `core/`, `core/base/`, `utils/`, `vectors/`, and all `vectors/*/` subdirectories. These were created as empty files so Python 2.7 can import packages. Do not delete them.

## External credentials (optional)
Some vectors need API keys configured in `core/ricco.ini`:
- **Flickr** (`flickr_by_radius`) — Flickr API key
- **Instagram** (`instagram_by_radius`) — Instagram client ID/secret or user/pass
- **Google** (`location_info`) — Google API key

Core vectors (`dns_info`, `dns_zone_transfer`, `http_grab_banner`, `iana_whois_info`, `domain_whois_info`, `ip_whois_info`, `subdomains_fuzzing`, `dirs_fuzzing`, `suffixes_fuzzing`, `mails_on_host`) work without any credentials.

## Dependencies
- Python 2.7 (via `python:2.7-slim` Docker image)
- pip packages in `requirements.txt`: dnspython, ipwhois, ipaddr, pythonwhois, futures, xmlutils, lxml
- `nmap` is needed for the `nmap_banner` vector (not installed in the base image)
