from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

from media_downloader import install


@pytest.fixture
def fake_mac(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "home"
    venv = tmp_path / "checkout" / ".venv"
    monkeypatch.setattr(install.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(install.Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(install.sys, "prefix", str(venv))
    return home


def test_chrome_launcher_lives_outside_the_browser_data_folder(fake_mac: Path) -> None:
    manifest_path = install.install("chrome", "jkflcccmckpakodmodoonlanhbcpnlfb")

    chrome_data = fake_mac / "Library" / "Application Support" / "Google" / "Chrome"
    assert manifest_path.parent == chrome_data / "NativeMessagingHosts"
    launcher = Path(json.loads(manifest_path.read_text())["path"])
    assert not launcher.is_relative_to(chrome_data)
    assert launcher.is_relative_to(Path(sys.prefix))
    assert os.access(launcher, os.X_OK)
    assert f'exec "{sys.executable}" -m media_downloader.host' in launcher.read_text()


def test_every_browser_points_at_the_same_launcher(fake_mac: Path) -> None:
    chrome = install.install("chrome", "jkflcccmckpakodmodoonlanhbcpnlfb")
    firefox = install.install("firefox", None)

    assert json.loads(chrome.read_text())["path"] == json.loads(firefox.read_text())["path"]
