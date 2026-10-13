#!/usr/bin/env python3
"""Minimal socket-based WHOIS client."""
import socket


class WhoisError(Exception):
    """Raised when a whois lookup fails or the domain is not registered."""


_NOT_FOUND_MARKERS = ("no match", "not found", "no entries found", "no data found")


def _query_server(server, query, timeout=10):
    try:
        return _connect_and_read(server, query, timeout)
    except OSError as e:
        raise WhoisError("whois query to %s failed" % server) from e


def _connect_and_read(server, query, timeout):
    with socket.create_connection((server, 43), timeout=timeout) as sock:
        sock.sendall((query + "\r\n").encode("utf-8"))
        chunks = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace")


def get_whois_raw(domain):
    """Return the raw whois text for a domain, following one IANA referral."""
    raw = _query_server("whois.iana.org", domain)
    referral = None
    for line in raw.splitlines():
        if line.lower().startswith("refer:"):
            referral = line.split(":", 1)[1].strip()
            break
    if referral:
        raw = _query_server(referral, domain)
    if any(marker in raw.lower() for marker in _NOT_FOUND_MARKERS):
        raise WhoisError("domain not found: %s" % domain)
    return raw
