"""Run the six independent checkouts in dependency order with staged local inputs."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys

PROJECTS = [
    "industrial-foundation-model-engineering",
    "engineering-llm-evaluation-framework",
    "llm-inference-performance-engineering",
    "industrial-predictive-maintenance-ml",
    "multimodal-engineering-document-intelligence",
    "sovereign-ai-mlops-platform",
]


def execute(root, inputs, output):
    root = root.resolve()
    inputs = inputs.resolve()
    output = output.resolve()
    paths = [root / p for p in PROJECTS]
    for d in paths:
        if not (d / "pyproject.toml").is_file():
            raise ValueError(f"Missing sibling checkout {d.name}")
    for f in [
        inputs / "energy.zip",
        inputs / "bert/model.safetensors",
        inputs / "smol/model.safetensors",
    ]:
        if not f.is_file():
            raise ValueError(f"Missing staged input {f.name}")
    output.mkdir(parents=True, exist_ok=False)
    env = {
        **os.environ,
        "HF_HUB_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "TRANSFORMERS_OFFLINE": "1",
        "LOCAL_MODEL": str(inputs / "smol"),
        "BERT_PATH": str(inputs / "bert"),
        "OMP_NUM_THREADS": "2",
        "RELEASE_KEY": secrets.token_hex(32),
        "PYTHONPATH": str(paths[1]),
        "MLFLOW_ENABLE_ASYNC_LOGGING": "false",
    }

    def run(index, module, *args):
        subprocess.run(
            [sys.executable, "-m", module, *map(str, args)],
            cwd=paths[index],
            env=env,
            check=True,
        )

    train = output / "training"
    run(0, "posttrain.experiment", "--out", train)
    run(0, "posttrain.alignment", train / "sft", output / "alignment")
    report = output / "qualification.json"
    run(1, "evaluation.score", train / "base.json", train / "dpo.json", report)
    rev = (inputs / "smol/revision.txt").read_text().strip()
    run(
        2,
        "serving.benchmark",
        "--model",
        inputs / "smol",
        "--revision",
        rev,
        "--adapter",
        train / "dpo",
        "--cases",
        train / "base.json",
        "--out",
        output / "cpu.json",
    )
    run(3, "condition.energy", inputs / "energy.zip", output / "energy.json")
    run(3, "condition.vibration", output / "vibration.json")
    run(4, "records.model", output / "cards")
    run(
        5,
        "lifecycle.qualify",
        train / "run.json",
        report,
        train / "dpo/adapter_model.safetensors",
        train / "dpo.json",
        train / "base.json",
        output / "registry.sqlite",
    )
    run(
        5,
        "integrations.mlflow_track",
        output / "mlflow",
        train / "run.json",
        report,
        train / "dpo",
        output / "tracking.json",
    )
    artifacts = [
        train / "run.json",
        report,
        output / "cpu.json",
        output / "energy.json",
        output / "vibration.json",
        output / "cards/report.json",
        output / "tracking.json",
        output / "alignment/metrics.json",
    ]
    index = {
        str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in artifacts
    }
    (output / "catalogue.json").write_text(json.dumps(index, indent=2) + "\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for k in ("checkouts", "inputs", "output"):
        p.add_argument(k, type=Path)
    a = p.parse_args()
    execute(a.checkouts, a.inputs, a.output)
