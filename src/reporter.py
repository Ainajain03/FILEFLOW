"""reporter.py - Logging setup and report generation/printing."""
import logging
from datetime import datetime
from pathlib import Path


def setup_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"fileflow_{datetime.now():%Y%m%d_%H%M%S}.log"
    logger = logging.getLogger("fileflow")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    return logger


def format_size(num_bytes: float) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def print_report(stats: dict, moved=None, skipped=None, failed=None):
    print("\nFILEFLOW ANALYSIS REPORT")
    print(f"Files scanned: {stats['total_count']}")
    print(f"Total storage: {format_size(stats['total_size'])}\n")
    for category, data in stats["by_category"].items():
        print(f"{category}: {data['count']} files — {format_size(data['size'])}")
    if moved is not None:
        print(f"\nFiles moved: {moved}\nFiles skipped: {skipped}\nFiles failed: {failed}")


def save_report(stats: dict, reports_dir: Path, moved=None, skipped=None, failed=None) -> Path:
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / f"report_{datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(report_file, "w") as f:
        f.write("FILEFLOW ANALYSIS REPORT\n")
        f.write(f"Files scanned: {stats['total_count']}\n")
        f.write(f"Total storage: {format_size(stats['total_size'])}\n\n")
        for category, data in stats["by_category"].items():
            f.write(f"{category}: {data['count']} files — {format_size(data['size'])}\n")
        if moved is not None:
            f.write(f"\nFiles moved: {moved}\nFiles skipped: {skipped}\nFiles failed: {failed}\n")
    return report_file