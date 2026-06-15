#!/usr/bin/env python3
"""Check if periodic reports are due. Output [FLYWHEEL] signal if any are missing.

Called by SessionStart hook. Checks for last week's weekly report and last
month's monthly report. If either is missing, outputs a signal that CLAUDE.md
routing picks up to trigger report generation.

Skips silently when:
- Cold start has not been run (no .claude/profiles/*.md)
- No work records exist yet (records/INDEX.md missing or empty)
"""

from datetime import date, timedelta
from pathlib import Path

# Guard: skip if cold start hasn't been run yet
PROFILES_DIR = Path(".claude/profiles")
if not any(PROFILES_DIR.glob("*.md")):
    exit(0)

# Guard: skip if no work records exist
INDEX_FILE = Path("records/INDEX.md")
if not INDEX_FILE.exists():
    exit(0)
index_content = INDEX_FILE.read_text()
# INDEX.md has a header row plus data rows. Empty = only header (2 lines max).
data_lines = [l for l in index_content.split("\n") if l.strip().startswith("|")]
if len(data_lines) <= 2:  # header separator + no data
    exit(0)

REPORTS_DIR = Path("records/_reports")
MISSING = []

today = date.today()

# Last week (Monday of the week before the current week)
days_since_monday = today.weekday()
last_monday = today - timedelta(days=days_since_monday + 7)
iso_year, iso_week, _ = last_monday.isocalendar()
weekly_file = REPORTS_DIR / f"{iso_year}-W{iso_week:02d}.md"

if not weekly_file.exists():
    MISSING.append(f"周报: {weekly_file}")

# Last month
first_of_month = today.replace(day=1)
last_day_of_prev_month = first_of_month - timedelta(days=1)
last_month = last_day_of_prev_month.strftime("%Y-%m")
monthly_file = REPORTS_DIR / f"{last_month}.md"

if not monthly_file.exists():
    MISSING.append(f"月报: {monthly_file}")

if MISSING:
    print()
    print("---")
    print("[FLYWHEEL] 以下工作报告尚未生成：")
    for m in MISSING:
        print(m)
    print("请在本次会话中生成。请读取 .claude/skills/flywheel/workflows/report.md 执行。")
    print("---")
    print()
