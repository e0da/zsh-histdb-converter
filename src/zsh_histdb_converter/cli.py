#!/usr/bin/env python3
"""Command-line interface for zsh-histdb-converter."""

import argparse
import os
import sys
from pathlib import Path
from .converter import convert_recent_history


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert zsh history to zsh-histdb format for Atuin import"
    )

    parser.add_argument(
        "history_file",
        nargs="?",
        default=os.path.expanduser("~/.histfile"),
        help="Path to zsh history file (default: ~/.histfile)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="zsh-history.db",
        help="Output database file (default: zsh-history.db)",
    )

    parser.add_argument(
        "-n",
        "--count",
        type=int,
        help="Number of recent entries to convert (default: all entries)",
    )

    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory to store the database (default: data)",
    )

    parser.add_argument(
        "--import-to-atuin",
        action="store_true",
        help="Automatically import the database to Atuin after conversion",
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.history_file):
        print(f"Error: History file '{args.history_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Create data directory if it doesn't exist
    data_dir = Path(args.data_dir)
    data_dir.mkdir(exist_ok=True)

    # Full path to output database
    db_path = data_dir / args.output

    print(f"Converting zsh history from: {args.history_file}")
    print(f"Output database: {db_path}")
    if args.count:
        print(f"Converting last {args.count} entries")
    else:
        print("Converting all entries")

    try:
        convert_recent_history(str(args.history_file), str(db_path), args.count)
        print("✅ Conversion completed successfully!")

        if args.import_to_atuin:
            print("Importing to Atuin...")
            import subprocess

            env = os.environ.copy()
            env["HISTDB_FILE"] = str(db_path.absolute())

            result = subprocess.run(
                ["atuin", "import", "zsh-hist-db"],
                env=env,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("✅ Successfully imported to Atuin!")
            else:
                print(f"❌ Failed to import to Atuin: {result.stderr}")
                sys.exit(1)
        else:
            print(f"To import to Atuin, run:")
            print(f"  HISTDB_FILE='{db_path.absolute()}' atuin import zsh-hist-db")

    except Exception as e:
        print(f"❌ Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
