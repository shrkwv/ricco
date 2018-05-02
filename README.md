![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg)
![Supported OS](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg)

#Ricco

Simple Reconnaissance Framework.

Description
============
Ricco is a simple and extensible framework for retrieving information about target.

Features
========

- DNS Information

- Photos by Location.

- Whois Information ( only in terminal mode currently).

- Fuzzing on suffixes, dirs, and subdomains.

- Mails For Host.

Examples
========

Run specified Strategy on Target:

```python ricco.py --target <TARGET> --strategy <STRATEGY>```

Run specified Vector on Target:

```python ricco.py --target <TARGET> --vector <VECTOR>```

Run specified Vector on Target:

```python ricco.py --target <TARGET> --vector <VECTOR> --vector-args <ARG>=<VALUE>```

Show list of all Strategies:

```python ricco.py --show-strategies```

Show list of all Vectors:

```python ricco.py --show-vectors```

Help on specified Strategy:

```python ricco.py --help-vector <VECTOR>```

Help on specified Vector:

```python ricco.py --help-vector <VECTOR>```

Output Results ad json:

```python ricco.py --target <TARGET> --strategy <STRATEGY> --output-json```


Currently Available Vectors:

| Vector              | Description                              | Arguments   |
|:--------------------|:-----------------------------------------|:------------|
| dirs_fuzzing        | Check dirs on host                       |             |
| suffixes_fuzzing    | Check suffixes for host.                 |             |
| iana_whois_info     | Get whois info from IANA.                |             |
| domain_whois_info   | Get whois info from domain whois.        |             |
| panoramio_by_box    | Search Panoramio for photos by location. | radius      |
| location_info       | Get Info About location                  |             |
| nmap_banner         | Get banners from nmap banner nse.        |             |
| dns_info            | Get information from dns server.         |             |
| dns_zone_transfer   | Try to Make Zone Transfer.               |             |
| http_grab_banner    | Get banner from http/https.              |             |
| flickr_by_radius    | Search Flickr for photos by location.    | radius      |
| ip_whois_info       | Get whois info from IPWHOIS              |             |
| mails_on_host       | Search for mails by host.                |             |
| subdomains_fuzzing  | Check subdomains for host.               |             |
| instagram_by_radius | Search Instagram for photos by location. | radius      |
| youtube_by_radius   | Search YouTube for photos by location.   | radius      |

Installation
============

- Clone this repository
- pip install requirements.txt.
- python ricco.py --help
