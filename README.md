![Supported Python versions](https://img.shields.io/badge/python-3.12+-blue.svg)
![Supported OS](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg)
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/uv-badge.json)

Ricco
=====

Simple Agile Reconnaissance Framework.

Description
===========

Ricco is a simple and extensible framework for retrieving information about target.
It is a Python 3 CLI whose dependencies are managed with [uv](https://docs.astral.sh/uv/).

Features
========

- DNS Information

- Whois Information ( only in terminal mode currently).

- Fuzzing on suffixes, dirs, and subdomains.

- Mails For Host.

- Photos by Location (Flickr, requires your own API key).

Examples
========

Run specified Strategy on Target:

```uv run python ricco.py --target <TARGET> --strategy <STRATEGY>```

Run specified Vector on Target:

```uv run python ricco.py --target <TARGET> --vector <VECTOR>```

Run specified Vector with arguments:

```uv run python ricco.py --target <TARGET> --vector <VECTOR> --vector-args <ARG>=<VALUE>```

Show list of all Strategies:

```uv run python ricco.py --show-strategies```

Show list of all Vectors:

```uv run python ricco.py --show-vectors```

Help on specified Vector:

```uv run python ricco.py --help-vector <VECTOR>```

Output Results as json:

```uv run python ricco.py --target <TARGET> --strategy <STRATEGY> --output-json```


Currently Available Vectors:

| Vector              | Description                              | Arguments   |
|:--------------------|:-----------------------------------------|:------------|
| dirs_fuzzing        | Check dirs on host                       |             |
| suffixes_fuzzing    | Check suffixes for host.                 |             |
| iana_whois_info     | Get whois info from IANA.                |             |
| domain_whois_info   | Get whois info from domain whois.        |             |
| location_info       | Get Info About location                  |             |
| nmap_banner         | Get banners from nmap banner nse.        |             |
| dns_info            | Get information from dns server.         |             |
| dns_zone_transfer   | Try to Make Zone Transfer.               |             |
| http_grab_banner    | Get banner from http/https.              |             |
| flickr_by_radius    | Search Flickr for photos by location.    | radius      |
| ip_whois_info       | Get whois info from IPWHOIS              |             |
| mails_on_host       | Search for mails by host.                |             |
| subdomains_fuzzing  | Check subdomains for host.               |             |

Installation
============

- Clone this repository
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- `uv sync`
- `uv run python ricco.py --help`

Some vectors need API keys configured in `core/ricco.ini` (Flickr, Google).

Web UI (Docker)
===============

A PHP/Apache web frontend is available via Docker (see `docker-compose.base44.yml`);
the container ships Python 3.12 and the dependency venv managed by uv:

```docker compose -f docker-compose.base44.yml up -d --build
# Preview at http://localhost:3000
```
