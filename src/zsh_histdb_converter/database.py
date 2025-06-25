"""Database module for creating and managing zsh-histdb compatible databases."""

import sqlite3
import socket
from typing import Dict, Any


def create_zsh_histdb(db_path: str) -> None:
    """Create a new zsh-histdb compatible database.

    Args:
        db_path: Path where the database file should be created
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the schema exactly as zsh-histdb does
    cursor.executescript("""
        CREATE TABLE commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            argv TEXT,
            UNIQUE(argv) ON CONFLICT IGNORE
        );

        CREATE TABLE places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host TEXT,
            dir TEXT,
            UNIQUE(host, dir) ON CONFLICT IGNORE
        );

        CREATE TABLE history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session INT,
            command_id INT REFERENCES commands (id),
            place_id INT REFERENCES places (id),
            exit_status INT,
            start_time INT,
            duration INT
        );

        PRAGMA user_version = 2;
    """)

    conn.commit()
    conn.close()


def add_history_entry(
    db_path: str,
    entry: Dict[str, Any],
    hostname: str = None,
    directory: str = None,
    session_id: int = 1,
) -> None:
    """Add a history entry to the zsh-histdb database.

    Args:
        db_path: Path to the database file
        entry: Dictionary with 'timestamp', 'duration', and 'command' keys
        hostname: Hostname where command was run (defaults to current hostname)
        directory: Directory where command was run (defaults to current directory)
        session_id: Session identifier
    """
    if hostname is None:
        hostname = socket.gethostname()

    if directory is None:
        import os

        directory = os.getcwd()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Insert command (or get existing id due to UNIQUE constraint)
        cursor.execute(
            "INSERT OR IGNORE INTO commands (argv) VALUES (?)", (entry["command"],)
        )
        cursor.execute("SELECT id FROM commands WHERE argv = ?", (entry["command"],))
        command_id = cursor.fetchone()[0]

        # Insert place (or get existing id due to UNIQUE constraint)
        cursor.execute(
            "INSERT OR IGNORE INTO places (host, dir) VALUES (?, ?)",
            (hostname, directory),
        )
        cursor.execute(
            "SELECT id FROM places WHERE host = ? AND dir = ?", (hostname, directory)
        )
        place_id = cursor.fetchone()[0]

        # Insert history entry
        # In zsh-histdb, exit_status defaults to 0, start_time is the timestamp
        cursor.execute(
            """
            INSERT INTO history (session, command_id, place_id, exit_status, start_time, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                session_id,
                command_id,
                place_id,
                0,
                entry["timestamp"],
                entry["duration"],
            ),
        )

        conn.commit()

    finally:
        conn.close()
