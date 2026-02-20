#!/usr/bin/env python3
"""Codex code-gen trigger.

Usage: python scripts/codex_codegen.py --prompt-file prompts/hello_world.txt --out-file generated/hello_world.py

This script expects OPENAI_API_KEY in the environment.
"""
import argparse
import os
import sys
from pathlib import Path

DEFAULT_PROMPT = """
# Task: generate a Python script.
# Requirements:
# - name the main function `main`
# - print "Hello, Life Studio AI!" when executed
# - include a `if __name__ == '__main__': main()` guard
"""


def load_prompt(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return DEFAULT_PROMPT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", default="prompts/hello_world.txt")
    parser.add_argument("--out-file", default="generated/hello_world.py")
    parser.add_argument(
        "--model",
        default=os.environ.get("CODEX_MODEL", "gpt-5.2"),
        help="OpenAI model id (default: gpt-5.2)",
    )
    args = parser.parse_args()

    prompt = load_prompt(Path(args.prompt_file))

    try:
        from openai import OpenAI
    except ImportError:  # pragma: no cover
        sys.exit("Install the OpenAI client: pip install openai")

    client = OpenAI()
    resp = client.chat.completions.create(
        model=args.model,
        messages=[
            {
                "role": "system",
                "content": "You generate only runnable code. Do not include markdown or prose.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    code = resp.choices[0].message.content
    out_path = Path(args.out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code, encoding="utf-8")
    print(f"Wrote {out_path.relative_to(Path.cwd()).as_posix()}")


if __name__ == "__main__":
    main()
