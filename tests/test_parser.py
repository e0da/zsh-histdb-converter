"""Test the zsh history parser."""

import tempfile
import os
import pytest
from zsh_histdb_converter.parser import parse_zsh_entry, read_recent_history


def test_parse_single_command():
    """Test parsing a single zsh history entry from a file."""
    # Create a temporary file with a single command
    history_content = ": 1736896969:0;ls -la\n"

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".histfile") as f:
        f.write(history_content)
        temp_file = f.name

    try:
        # Use read_recent_history to read the single entry
        entries = read_recent_history(temp_file, n=1)

        # Should return exactly one entry
        assert len(entries) == 1

        # Check the entry content
        entry = entries[0]
        assert entry["timestamp"] == 1736896969
        assert entry["duration"] == 0
        assert entry["command"] == "ls -la"

    finally:
        os.unlink(temp_file)


def test_parse_simple_zsh_entry():
    """Test parsing a simple zsh history entry."""
    entry = ": 1609459200:0;ls -la"
    result = parse_zsh_entry(entry)

    expected = {"timestamp": 1609459200, "duration": 0, "command": "ls -la"}

    assert result == expected


def test_read_recent_history():
    """Test reading the most recent N entries from zsh history."""
    # Create a temporary history file with test data
    history_content = """
: 1609459200:0;ls -la
: 1609459260:1;cd /home/user
: 1609459320:0;git status
: 1609459380:2;vim test.py
: 1609459440:0;python test.py
""".strip()

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".histfile") as f:
        f.write(history_content)
        temp_file = f.name

    try:
        # Read most recent 3 entries
        recent_entries = read_recent_history(temp_file, n=3)

        assert len(recent_entries) == 3

        # Should be in reverse chronological order (most recent first)
        assert recent_entries[0]["command"] == "python test.py"
        assert recent_entries[0]["timestamp"] == 1609459440

        assert recent_entries[1]["command"] == "vim test.py"
        assert recent_entries[1]["timestamp"] == 1609459380

        assert recent_entries[2]["command"] == "git status"
        assert recent_entries[2]["timestamp"] == 1609459320

    finally:
        os.unlink(temp_file)
