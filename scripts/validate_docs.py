"""Validate the document deliverable without changing the reference application."""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "e7f6311b96ee3b21bf8cb7077f53a6e4045143eb"
errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    required = ["README.md", "docs/PRD.md", "docs/RFC.md", "docs/FDD.md", "docs/TRACKER.md"]
    for name in required:
        check((ROOT / name).is_file(), f"Missing document: {name}")
    if errors:
        return report()
    # Compare tracked original bytes directly; catches unstaged changes too.
    protected = git("ls-tree", "-r", "--name-only", BASE, "--", "TRANSCRICAO.md", "src", "prisma", "tests").decode().splitlines()
    for name in protected:
        file = ROOT / name
        check(file.is_file() and file.read_bytes() == git("show", f"{BASE}:{name}"), f"Protected file changed: {name}")
    current = {str(f.relative_to(ROOT)) for folder in ("src", "prisma", "tests") for f in (ROOT / folder).rglob("*") if f.is_file()}
    check(current == set(protected) - {"TRANSCRICAO.md"}, "Protected directories contain added/missing files")
    adrs = sorted((ROOT / "docs/adrs").glob("ADR-*.md"))
    check(len(adrs) == 6, "Expected six ADRs")
    for file in adrs:
        check(bool(re.fullmatch(r"ADR-\d{3}-[a-z0-9-]+\.md", file.name)), f"Bad ADR name: {file.name}")
        for heading in ("Status", "Contexto", "Decisão", "Alternativas Consideradas", "Consequências"):
            check(f"## {heading}" in file.read_text(), f"{file.name}: missing {heading}")
    docs = [ROOT / name for name in required] + adrs
    json_examples = 0
    for file in docs:
        content = file.read_text()
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if re.match(r"[a-z]+://", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            check((file.parent / target).exists(), f"Broken link in {file.name}: {target}")
        for block in re.findall(r"```json\s*\n(.*?)```", content, re.S):
            json_examples += 1
            try:
                json.loads(block)
                check(True, "JSON valid")
            except json.JSONDecodeError as error:
                check(False, f"Invalid JSON in {file.name}: {error}")
    check(json_examples >= 8, "Insufficient request/response JSON examples")
    tracker = (ROOT / "docs/TRACKER.md").read_text()
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in tracker.splitlines() if re.match(r"\| [RC]\d{2} \|", line)]
    check(len(rows) == 68, "Tracker inventory must contain 68 groups")
    check(len({row[0] for row in rows}) == len(rows), "Duplicate tracker IDs")
    transcript = (ROOT / "TRANSCRICAO.md").read_text()
    sources = {"TRANSCRICAO": 0, "CODIGO": 0}
    for row in rows:
        check(len(row) == 6, f"Invalid tracker columns: {row[0]}")
        if len(row) != 6:
            continue
        source, location = row[4:6]
        check(source in sources, f"Invalid source: {source}")
        if source not in sources:
            continue
        sources[source] += 1
        if source == "TRANSCRICAO":
            check(bool(re.fullmatch(r"\[\d{2}:\d{2}\] \w+", location)), f"Bad timestamp/speaker: {location}")
            check(location + ":" in transcript, f"Source not found: {location}")
        else:
            check((ROOT / location.strip("`")).is_file(), f"Code path not found: {location}")
    check(bool(rows) and sources["TRANSCRICAO"] / len(rows) >= 0.7, "Less than 70% transcript rows")
    check(sources["CODIGO"] >= 5, "Fewer than five code references")
    fdd = (ROOT / "docs/FDD.md").read_text()
    for heading in ("Contexto", "Objetivos", "Escopo", "Integração com o sistema existente", "Contratos públicos", "Erros", "Observabilidade", "Dependências"):
        check(f"## {heading}" in fdd, f"FDD missing {heading}")
    check(len(set(re.findall(r"WEBHOOK_[A-Z_]+", fdd))) >= 4, "Missing domain error matrix")
    readme = (ROOT / "README.md").read_text()
    check(readme.count("```text") >= 2, "README needs two prompt blocks")
    check("Três ciclos" in readme, "README iteration record missing")
    print(f"Tracker: {sources['TRANSCRICAO']}/{len(rows)} transcript rows; {sources['CODIGO']} code rows; JSON examples: {json_examples}")
    return report()


def report():
    for message in errors:
        print(f"FAIL: {message}", file=sys.stderr)
    print(f"{'FAIL' if errors else 'PASS'}: {checks} document checks, {len(errors)} failures")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
