"""Main converter module for converting zsh history to zsh-histdb format."""

from typing import Optional
from .parser import read_recent_history
from .database import create_zsh_histdb, add_history_entry


def convert_recent_history(
    history_file: str, db_file: str, count: Optional[int] = None
) -> None:
    """Convert recent zsh history entries to a zsh-histdb compatible database.

    Args:
        history_file: Path to the zsh history file
        db_file: Path where the database should be created
        count: Number of recent entries to convert (None for all entries)
    """
    # Create the database
    create_zsh_histdb(db_file)

    # Read the recent history entries
    entries = read_recent_history(history_file, count)

    # Convert and add each entry to the database
    for parsed_entry in entries:
        # entries are already parsed by read_recent_history
        # Use default hostname and directory for now
        # In a real implementation, we might want to make these configurable
        add_history_entry(db_file, parsed_entry)
