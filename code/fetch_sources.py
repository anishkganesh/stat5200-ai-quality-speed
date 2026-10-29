"""Fetch the pinned public inputs; never execute downloaded code."""
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "sources/manifest.json").read_text(encoding="utf-8"))
for item in manifest["files"]:
    destination = (ROOT / item["path"]).resolve()
    if not destination.is_relative_to(ROOT):
        raise ValueError("Input destination must remain inside the repository")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        payload = destination.read_bytes()
        if hashlib.sha256(payload).hexdigest() == item["sha256"]:
            print("Verified local input:", item["path"])
            continue
    with urllib.request.urlopen(item["download_url"], timeout=120) as response:
        payload = response.read()
    if len(payload) != item["bytes"] or hashlib.sha256(payload).hexdigest() != item["sha256"]:
        raise ValueError("Downloaded input failed size/hash check: " + item["path"])
    destination.write_bytes(payload)
    print("Downloaded and verified:", item["path"])
