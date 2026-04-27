from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.bild.har_endpoints import (
    extract_endpoint_records,
    load_har,
    records_to_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract endpoint candidates from HAR without exposing secrets."
    )
    parser.add_argument(
        "--har-file",
        required=True,
        help="Path to HAR JSON file exported from a headed authenticated session.",
    )
    parser.add_argument(
        "--host-contains",
        default="leroymerlin",
        help="Case-insensitive hostname substring filter.",
    )
    parser.add_argument(
        "--output-markdown",
        default="",
        help="Optional output markdown file path.",
    )
    args = parser.parse_args()

    har_path = Path(args.har_file)
    if not har_path.exists():
        print(f"HAR file not found: {har_path}")
        return 1

    try:
        payload = load_har(har_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Failed to load HAR file: {error}")
        return 1
    records = extract_endpoint_records(payload, host_contains=args.host_contains)
    markdown_output = records_to_markdown(records)
    print(markdown_output)

    if args.output_markdown:
        output_path = Path(args.output_markdown)
        try:
            output_path.write_text(markdown_output, encoding="utf-8")
        except OSError as error:
            print(f"Failed to write markdown output: {error}")
            return 1
        print(f"\nWrote endpoint markdown to: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
