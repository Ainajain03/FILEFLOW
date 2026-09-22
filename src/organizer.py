"""organizer.py - Move files into category folders, handling duplicate names."""
import shutil
from pathlib import Path


def unique_destination(dest_folder: Path, filename: str) -> Path:
    dest = dest_folder / filename
    if not dest.exists():
        return dest
    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 1
    while True:
        candidate = dest_folder / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_files(files_with_categories, base_dir: Path, logger):
    moved, skipped, failed = 0, 0, 0
    for scanned_file, category in files_with_categories:
        dest_folder = base_dir / category
        try:
            dest_folder.mkdir(exist_ok=True)
            destination = unique_destination(dest_folder, scanned_file.name)
            shutil.move(str(scanned_file.path), str(destination))
            logger.info(f"MOVED {scanned_file.name} -> {category}\\{destination.name}")
            moved += 1
        except Exception as e:
            logger.error(f"FAILED {scanned_file.name}: {e}")
            failed += 1
    return moved, skipped, failed