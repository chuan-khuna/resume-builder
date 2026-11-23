# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6", "jsonschema>=4.23"]
# ///
"""Check resume YAML files against data/resume.schema.json.

    uv run scripts/check.py            # data/resume.yml and every versions/*/resume.yml
    uv run scripts/check.py FILE...    # only these files

Also fails on duplicate keys, which YAML parsers otherwise accept silently
(the second value wins), and on unquoted values such as `no` or `2025` that
YAML reads as a boolean or number where the schema wants text.
"""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "data" / "resume.schema.json"


class StrictLoader(yaml.SafeLoader):
    """SafeLoader that rejects a key repeated in the same mapping."""


def _mapping(loader: StrictLoader, node: yaml.MappingNode) -> dict:
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node)
        if key in seen:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", key_node.start_mark
            )
        seen.add(key)
    return loader.construct_mapping(node)


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def where(path) -> str:
    """JSON path like experiences[0].bullets[2].text."""
    out = ""
    for part in path:
        out += f"[{part}]" if isinstance(part, int) else f".{part}"
    return out.lstrip(".") or "(top level)"


def check(file: Path, validator: Draft202012Validator) -> list[str]:
    try:
        data = yaml.load(file.read_text(encoding="utf-8"), Loader=StrictLoader)
    except yaml.YAMLError as e:
        return [f"YAML: {e}"]
    if data is None:
        return ["file is empty"]
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    return [f"{where(e.absolute_path)}: {e.message}" for e in errors]


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    if len(sys.argv) > 1:
        files = [Path(f).resolve() for f in sys.argv[1:]]
    else:
        files = [ROOT / "data" / "resume.yml", *sorted(ROOT.glob("versions/*/resume.yml"))]

    failed = 0
    for file in files:
        name = file.relative_to(ROOT) if file.is_relative_to(ROOT) else file
        problems = check(file, validator) if file.exists() else ["file not found"]
        if problems:
            failed += 1
            print(f"FAIL {name}")
            for p in problems:
                print(f"  {p}")
        else:
            print(f"ok   {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
