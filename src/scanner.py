"""scanner.py - Scan a folder and return basic file objects. Works the same on Windows via pathlib."""
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ScannedFile:
    name: str
    path: Path
    extension: str
    size: int


def scan_directory(directory: str) -> list[ScannedFile]:
    target = Path(directory)
    if not target.exists() or not target.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a valid folder.")

    files = []
    for entry in target.iterdir():
        if entry.is_file():
            files.append(
                ScannedFile(
                    name=entry.name,
                    path=entry,
                    extension=entry.suffix.lower(),
                    size=entry.stat().st_size,
                )
            )
    return files