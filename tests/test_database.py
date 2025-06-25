import pytest
import sqlite3
import tempfile
import os
from zsh_histdb_converter.database import create_zsh_histdb


def test_create_empty_zsh_histdb():
    """Test creating an empty zsh-histdb compatible database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        # Create the database
        create_zsh_histdb(db_path)

        # Verify the database exists and has the correct schema
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check that all required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = {"commands", "places", "history"}
        # SQLite automatically creates sqlite_sequence for AUTOINCREMENT
        actual_tables = set(tables) - {"sqlite_sequence"}
        assert actual_tables == expected_tables

        # Check the schema of each table
        cursor.execute("PRAGMA table_info(commands)")
        commands_schema = cursor.fetchall()
        assert len(commands_schema) == 2  # id, argv

        cursor.execute("PRAGMA table_info(places)")
        places_schema = cursor.fetchall()
        assert len(places_schema) == 3  # id, host, dir

        cursor.execute("PRAGMA table_info(history)")
        history_schema = cursor.fetchall()
        assert (
            len(history_schema) == 7
        )  # id, session, command_id, place_id, exit_status, start_time, duration

        conn.close()

    finally:
        os.unlink(db_path)


def test_add_history_entry():
    """Test adding a history entry to the database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        # Create the database
        create_zsh_histdb(db_path)

        # Add a history entry
        from zsh_histdb_converter.database import add_history_entry

        entry = {"timestamp": 1609459200, "duration": 0, "command": "ls -la"}

        add_history_entry(
            db_path, entry, hostname="testhost", directory="/tmp", session_id=1
        )

        # Verify the entry was added
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM commands")
        assert cursor.fetchone()[0] == 1

        cursor.execute("SELECT COUNT(*) FROM places")
        assert cursor.fetchone()[0] == 1

        cursor.execute("SELECT COUNT(*) FROM history")
        assert cursor.fetchone()[0] == 1

        # Check the actual data
        cursor.execute("""
            SELECT c.argv, p.host, p.dir, h.exit_status, h.start_time, h.duration
            FROM history h
            JOIN commands c ON h.command_id = c.id
            JOIN places p ON h.place_id = p.id
        """)

        result = cursor.fetchone()
        assert result == ("ls -la", "testhost", "/tmp", 0, 1609459200, 0)

        conn.close()

    finally:
        os.unlink(db_path)
