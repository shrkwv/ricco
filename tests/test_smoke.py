import json
import socket
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
RICCO = REPO_ROOT / "ricco.py"


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
