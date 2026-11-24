#!/usr/bin/env python3
"""Download the open-access references listed in docs/refs/MANIFESTO.csv.

For every row with ``acesso == "aberto"`` and a ``url_download``, each path in
``arquivo_local`` (relative to docs/refs/) that does not exist yet is fetched.
``arquivo_local`` and ``url_download`` may hold several ``;``-separated values
(e.g. several versions of one work); a single URL is reused for every path.
Existing files are never overwritten. Paid, blocked and book rows are skipped.

The PDFs stay out of git (docs/refs/ is gitignored); only the manifest is
versioned, so this script rebuilds the folder on a new machine.

Usage:
    python scripts/fetch_refs.py --dry-run
    python scripts/fetch_refs.py
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REFS = REPO / "docs" / "refs"
MANIFEST = REFS / "MANIFESTO.csv"
USER_AGENT = "refs-fetcher/1.0"
PAUSE_S = 3.0
TIMEOUT_S = 120


def split(field: str) -> list[str]:
    return [part.strip() for part in field.split(";") if part.strip()]


def plan(manifest: Path) -> tuple[list[tuple[Path, str]], list[str]]:
    """Return (downloads to do, skipped-row messages)."""
    todo: list[tuple[Path, str]] = []
    skipped: list[str] = []
    with manifest.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            files = split(row["arquivo_local"])
            urls = split(row["url_download"])
            title = row["titulo_curto"]
            if row["acesso"] != "aberto":
                if not files or not all((REFS / f).exists() for f in files):
                    skipped.append(f"[{row['acesso']}] {title}: {row['identificador']}")
                continue
            if not files or not urls:
                missing = [f for f in files if not (REFS / f).exists()]
                if not files or missing:
                    skipped.append(f"[sem URL] {title}")
                continue
            if len(urls) not in (1, len(files)):
                skipped.append(f"[manifesto inválido] {title}: {len(files)} arquivos, {len(urls)} URLs")
                continue
            for i, rel in enumerate(files):
                target = (REFS / rel).resolve()
                if REFS.resolve() not in target.parents:
                    skipped.append(f"[caminho fora de docs/refs] {rel}")
                    continue
                if not target.exists():
                    todo.append((target, urls[0] if len(urls) == 1 else urls[i]))
    return todo, skipped


def fetch(url: str, target: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        raise ValueError("a resposta não é um PDF (página de erro ou bloqueio?)")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".part")
    tmp.write_bytes(data)
    tmp.replace(target)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--dry-run", action="store_true", help="list what would be downloaded and exit")
    args = ap.parse_args()

    todo, skipped = plan(args.manifest)
    for msg in skipped:
        print(f"não baixável: {msg}")
    print(f"{len(todo)} arquivo(s) a baixar")
    if args.dry_run:
        for target, url in todo:
            print(f"  {url} -> {target.relative_to(REPO)}")
        return 0

    failures = 0
    for n, (target, url) in enumerate(todo):
        if n:
            time.sleep(PAUSE_S)
        if target.exists():  # another row may have created it meanwhile
            continue
        try:
            fetch(url, target)
            print(f"ok   {target.relative_to(REPO)}")
        except (urllib.error.URLError, ValueError, OSError) as exc:
            failures += 1
            print(f"ERRO {target.relative_to(REPO)} <- {url}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
