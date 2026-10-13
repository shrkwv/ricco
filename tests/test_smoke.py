import json
import socket
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
RICCO = REPO_ROOT / "ricco.py"
sys.path.insert(0, str(REPO_ROOT))


def run_ricco(*args):
    return subprocess.run(
        [sys.executable, str(RICCO), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_show_vectors_lists_registered_vectors():
    result = run_ricco("--show-vectors")
    assert result.returncode == 0
    assert "dns_info" in result.stdout
    assert "dirs_fuzzing" in result.stdout


def test_help_exits_zero():
    result = run_ricco("--help")
    assert result.returncode == 0


def _dns_available():
    try:
        socket.gethostbyname("example.com")
        return True
    except OSError:
        return False


def test_dns_info_json_output():
    if not _dns_available():
        pytest.skip("network unavailable")
    result = run_ricco("--target", "example.com", "--vector", "dns_info", "--output-json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert "dns_info" in payload


def test_ip_whois_info_runs():
    """execute() must not hit a missing ipwhois method, which the manager swallows."""
    if not _dns_available():
        pytest.skip("network unavailable")
    from vectors.infogather.ip_whois_info import ip_whois_info

    vector = ip_whois_info()
    vector.prepare("8.8.8.8", None)
    vector.execute()
    assert isinstance(vector.result, dict) and vector.result
