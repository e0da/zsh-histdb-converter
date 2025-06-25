"""Parser for zsh history entries."""

import re
from typing import Dict, Optional, List


def parse_zsh_entry(entry: str) -> Optional[Dict[str, any]]:
    """Parse a single zsh history entry.

    Args:
        entry: A zsh history line in format ": timestamp:duration;command"

    Returns:
        Dict with timestamp, duration, and command, or None if invalid
    """
    # Pattern matches ": timestamp:duration;command"
    pattern = r"^: (\d+):(\d+);(.*)$"
    match = re.match(pattern, entry)

    if not match:
        return None

    timestamp = int(match.group(1))
    duration = int(match.group(2))
    command = match.group(3)

    return {"timestamp": timestamp, "duration": duration, "command": command}


def read_recent_history(
    history_file: str, n: Optional[int] = 10
) -> List[Dict[str, any]]:
    """Read the most recent N entries from a zsh history file.

    Args:
        history_file: Path to the zsh history file
        n: Number of recent entries to return (None for all entries)

    Returns:
        List of parsed history entries, most recent first
    """
    entries = []

    with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Process lines in reverse order to get most recent first
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue

        parsed = parse_zsh_entry(line)
        if parsed:
            entries.append(parsed)

        # Stop when we have enough entries (unless n is None)
        if n is not None and len(entries) >= n:
            break

    return entries
