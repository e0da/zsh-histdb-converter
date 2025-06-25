import pytest
import tempfile
import os
from zsh_histdb_converter.converter import convert_recent_history


def test_convert_recent_history():
    """Test converting recent zsh history entries to a database."""
    # Create a temporary zsh history file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(": 1609459200:0;ls -la\n")
        f.write(": 1609459210:5;cd /tmp\n")
        f.write(": 1609459220:1;pwd\n")
        history_file = f.name

    # Create a temporary database file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_file = f.name

    try:
        # Convert the recent history (last 2 entries)
        convert_recent_history(history_file, db_file, count=2)

        # Verify the database was created and contains the expected entries
        import sqlite3

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Should have 2 commands
        cursor.execute("SELECT COUNT(*) FROM commands")
        assert cursor.fetchone()[0] == 2

        # Should have 1 place (same host/dir for all)
        cursor.execute("SELECT COUNT(*) FROM places")
        assert cursor.fetchone()[0] == 1

        # Should have 2 history entries
        cursor.execute("SELECT COUNT(*) FROM history")
        assert cursor.fetchone()[0] == 2

        # Check the commands are the most recent ones
        cursor.execute("SELECT argv FROM commands ORDER BY id")
        commands = [row[0] for row in cursor.fetchall()]
        assert commands == ["pwd", "cd /tmp"]  # The last 2 commands (most recent first)

        conn.close()

    finally:
        os.unlink(history_file)
        os.unlink(db_file)


def test_convert_all_history():
    """Test converting all zsh history entries to a database."""
    # Create a temporary zsh history file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(": 1609459200:0;ls -la\n")
        f.write(": 1609459210:5;cd /tmp\n")
        f.write(": 1609459220:1;pwd\n")
        history_file = f.name

    # Create a temporary database file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_file = f.name

    try:
        # Convert all history
        convert_recent_history(history_file, db_file, count=None)

        # Verify the database was created and contains all entries
        import sqlite3

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Should have 3 commands
        cursor.execute("SELECT COUNT(*) FROM commands")
        assert cursor.fetchone()[0] == 3

        # Should have 3 history entries
        cursor.execute("SELECT COUNT(*) FROM history")
        assert cursor.fetchone()[0] == 3

        # Check all commands are present
        cursor.execute("SELECT argv FROM commands ORDER BY id")
        commands = [row[0] for row in cursor.fetchall()]
        assert commands == ["pwd", "cd /tmp", "ls -la"]  # Most recent first

        conn.close()

    finally:
        os.unlink(history_file)
        os.unlink(db_file)
