"""analyzer.py - Compute statistics over classified files."""
from collections import defaultdict


def analyze(files_with_categories):
    """files_with_categories: list of (ScannedFile, category) tuples."""
    stats = defaultdict(lambda: {"count": 0, "size": 0})
    total_count = 0
    total_size = 0
    all_files = []

    for scanned_file, category in files_with_categories:
        stats[category]["count"] += 1
        stats[category]["size"] += scanned_file.size
        total_count += 1
        total_size += scanned_file.size
        all_files.append(scanned_file)

    all_files.sort(key=lambda f: f.size, reverse=True)

    return {
        "total_count": total_count,
        "total_size": total_size,
        "by_category": dict(stats),
        "largest_files": all_files[:5],
    }