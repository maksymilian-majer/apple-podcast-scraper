#!/usr/bin/env python3
"""Remove timestamp lines from YouTube transcript exports."""

import re
import sys


def strip_timestamps(text):
    """Remove lines that are just timestamps (e.g., 0:01, 1:23:45)."""
    lines = text.split("\n")
    # Match timestamps like 0:01, 1:23, 10:45, 1:23:45
    timestamp_pattern = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")

    cleaned = [line for line in lines if not timestamp_pattern.match(line.strip())]
    return "\n".join(cleaned)


def main():
    if len(sys.argv) < 2:
        print("Usage: python strip_timestamps.py <input_file> [output_file]")
        print("       If no output file specified, prints to stdout")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned = strip_timestamps(content)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"[+] Cleaned transcript saved to '{output_file}'")
    else:
        print(cleaned)


if __name__ == "__main__":
    main()
