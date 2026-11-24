"""Create only new, public GitHub repositories and publish the archived milestone."""

import argparse
import json
from pathlib import Path
import subprocess


def call(*args, cwd=None):
    return subprocess.run(
        args, cwd=cwd, text=True, check=True, capture_output=True
    ).stdout.strip()


def main(archive: Path, publish: bool):
    manifest = json.loads((archive / "delivery.json").read_text())
    login = call("gh", "api", "user", "--jq", ".login")
    if login.casefold() != manifest["account"].casefold():
        raise ValueError(f"Expected {manifest['account']}, logged in as {login}")
    existing = set(
        call(
            "gh",
            "api",
            "--paginate",
            "user/repos?affiliation=owner&per_page=100",
            "--jq",
            ".[].full_name",
        )
        .casefold()
        .splitlines()
    )
    journal_path = archive / "publication-receipts.json"
    receipts = json.loads(journal_path.read_text()) if journal_path.exists() else {}
    plans = []
    for item in manifest["repositories"]:
        name = item["name"]
        repo = f"{login}/{name}"
        bundle = archive / "history" / (name + ".bundle")
        refs = call("git", "bundle", "list-heads", str(bundle)).splitlines()
        if item["commit"] + " refs/heads/main" not in refs:
            raise ValueError("Bundle commit mismatch")
        if repo.casefold() in existing:
            if repo in receipts and receipts[repo] == call(
                "gh", "api", "repos/" + repo, "--jq", ".node_id"
            ):
                branches = json.loads(call("gh", "api", "repos/" + repo + "/branches"))
                if not branches:
                    plans.append((item, "resume empty repository"))
                    continue
            remote = call(
                "gh",
                "api",
                "repos/" + repo + "/git/ref/heads/main",
                "--jq",
                ".object.sha",
            )
            if remote != item["commit"]:
                raise ValueError(
                    f"Name conflict at {repo}. Existing repository preserved."
                )
            plans.append((item, "already published"))
        else:
            plans.append((item, "create"))
    if publish:
        call("gh", "auth", "setup-git")
    for item, status in plans:
        name = item["name"]
        repo = f"{login}/{name}"
        print(f"{status}: {repo}", flush=True)
        if not publish or (status == "already published" and repo not in receipts):
            continue
        if status in {"create", "resume empty repository"}:
            temp = archive / "publish-checkouts" / name
            if not temp.exists():
                call(
                    "git",
                    "clone",
                    "--branch",
                    "main",
                    str(archive / "history" / (name + ".bundle")),
                    str(temp),
                )
            if call("git", "rev-parse", "HEAD", cwd=temp) != item["commit"]:
                raise ValueError("Checkout differs from delivery")
            if status == "create":
                created = json.loads(
                    call(
                        "gh",
                        "api",
                        "user/repos",
                        "-X",
                        "POST",
                        "-f",
                        "name=" + name,
                        "-f",
                        "description=" + item["description"],
                        "-F",
                        "private=false",
                        "-F",
                        "auto_init=false",
                    )
                )
                receipts[repo] = created["node_id"]
                staged = journal_path.with_suffix(".tmp")
                staged.write_text(json.dumps(receipts, indent=2))
                staged.replace(journal_path)
            # Use explicit URLs so the local clone retains its read-only bundle origin.
            call(
                "git",
                "push",
                "--atomic",
                f"https://github.com/{repo}.git",
                "refs/heads/main:refs/heads/main",
                "refs/tags/v0.1.0:refs/tags/v0.1.0",
                cwd=temp,
            )
        actual = call(
            "gh", "api", f"repos/{repo}/git/ref/heads/main", "--jq", ".object.sha"
        )
        if actual != item["commit"]:
            raise RuntimeError(f"Publication verification failed for {repo}")
        call("gh", "repo", "edit", repo, "--add-topic", ",".join(item["topics"]))
        releases = json.loads(call("gh", "api", f"repos/{repo}/releases"))
        if not any(r["tag_name"] == "v0.1.0" for r in releases):
            call(
                "gh",
                "release",
                "create",
                "v0.1.0",
                "--repo",
                repo,
                "--verify-tag",
                "--prerelease",
                "--title",
                "v0.1.0 research milestone",
                "--notes",
                "CPU research milestone. See README, measured reports and outstanding verification gates.",
            )
        print(
            call(
                "gh",
                "run",
                "list",
                "--repo",
                repo,
                "--commit",
                actual,
                "--limit",
                "3",
                "--json",
                "status,conclusion,url",
            )
        )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path)
    p.add_argument("--publish", action="store_true")
    a = p.parse_args()
    main(a.archive.resolve(), a.publish)
