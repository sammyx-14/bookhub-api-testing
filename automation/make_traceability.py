# make_traceability.py
# Builds TRACEABILITY.md from the test code. Reads the files only: no API calls.
# Run from the automation folder:  python make_traceability.py

import ast
import pathlib
import re


def markers(node):
    found = []
    for decorator in node.decorator_list:
        text = ast.unparse(decorator)
        for name in ("negative", "security", "e2e"):
            if text == f"pytest.mark.{name}":
                found.append(name)
    return ", ".join(found) or "-"


rows = []
for path in sorted(pathlib.Path("tests").rglob("test_*.py")):
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            doc = (ast.get_docstring(node) or "").splitlines()[0]
            match = re.match(r"(TC-\d+|E2E-\d+)", doc)
            summary = doc.split(":", 1)[1].strip() if ":" in doc else doc
            rows.append((match.group(1), summary,
                        f"`{node.name}`", f"`{path}`", markers(node)))

rows.sort(key=lambda r: (r[0].startswith("E2E"), r[0]))

lines = [
    "# Traceability: test case ID to automated test",
    "",
    "Generated from the test code by `make_traceability.py`. Each row links a test",
    "case ID (as used in the Test Cases document) to the pytest function that checks it.",
    "",
    "| ID | What it verifies | Test function | File | Markers |",
    "|---|---|---|---|---|",
]
for row in rows:
    lines.append("| " + " | ".join(row) + " |")
lines += [
    "",
    f"{len(rows)} test functions. TC-004 is covered by two functions "
    "(the weak-password set and the 8-character boundary).",
    "",
]
pathlib.Path("TRACEABILITY.md").write_text("\n".join(lines))
print("written", len(rows), "rows")
