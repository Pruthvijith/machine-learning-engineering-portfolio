"""Stage only the named files from immutable public model revisions and verify bytes."""

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen
from urllib.parse import quote

SOURCES = {
    "smol": (
        "HuggingFaceTB/SmolLM2-135M",
        "93efa2f097d58c2a74874c7e644dbc9b0cee75a2",
        {
            "config.json",
            "model.safetensors",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "generation_config.json",
        },
    ),
    "bert": (
        "google/bert_uncased_L-2_H-128_A-2",
        "30b0a37ccaaa32f332884b96992754e246e48c5f",
        {"config.json", "vocab.txt", "model.safetensors"},
    ),
}
ENERGY = (
    "https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip"
)
ENERGY_SHA = "2fccf354445d886e7917620b0195db1f3e3e34d5a067a93b844694a4c561255a"


def file_hash(path, algorithm, git=False):
    h = hashlib.new(algorithm)
    if git:
        h.update(f"blob {path.stat().st_size}\0".encode())
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def download(url, path, expected, git=False):
    algorithm = "sha1" if git else "sha256"
    if path.exists() and file_hash(path, algorithm, git) == expected:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        staged = Path(output.name)
    try:
        with (
            urlopen(
                Request(url, headers={"User-Agent": "engineering-portfolio/0.1"}),
                timeout=120,
            ) as response,
            staged.open("wb") as handle,
        ):
            while chunk := response.read(1024 * 1024):
                handle.write(chunk)
        if file_hash(staged, algorithm, git) != expected:
            raise ValueError("Downloaded file failed integrity check")
        staged.replace(path)
    finally:
        staged.unlink(missing_ok=True)


def stage(name, target):
    repo, rev, files = SOURCES[name]
    with urlopen(
        f"https://huggingface.co/api/models/{repo}/revision/{rev}?blobs=true",
        timeout=30,
    ) as r:
        meta = json.load(r)
    if meta["sha"] != rev:
        raise ValueError("Revision changed")
    available = {f["rfilename"]: f for f in meta["siblings"]}
    for name in sorted(files):
        f = available[name]
        lfs = f.get("lfs", {})
        download(
            f"https://huggingface.co/{repo}/resolve/{rev}/{quote(name)}",
            target / name,
            lfs.get("sha256") or f["blobId"],
            not bool(lfs),
        )
    (target / "revision.txt").write_text(rev + "\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("root", type=Path)
    p.add_argument("items", nargs="+", choices=["smol", "bert", "energy"])
    args = p.parse_args()
    for item in args.items:
        if item == "energy":
            download(ENERGY, args.root / "energy.zip", ENERGY_SHA)
        else:
            stage(item, args.root / item)
