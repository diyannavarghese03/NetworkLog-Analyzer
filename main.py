import sys
from pathlib import Path

from parser import read_logs, parse_logs
from analyzer import analyze_logs
from report import print_report, save_report

ROOT_DIR = Path(__file__).resolve().parent

if len(sys.argv) > 1:
    log_file = Path(sys.argv[1])
    if not log_file.is_absolute():
        log_file = ROOT_DIR / log_file
else:
    log_file = ROOT_DIR / "logs" / "sample.log"

try:
    logs = read_logs(str(log_file))
    parsed_logs = parse_logs(logs)
    results = analyze_logs(parsed_logs)
except FileNotFoundError:
    print(f"Error: log file not found: {log_file}")
    raise SystemExit(1)

print_report(results)

report_dir = ROOT_DIR / "reports"
report_dir.mkdir(exist_ok=True)
save_report(results, str(report_dir / "report.txt"))

print(f"\nReport saved to {report_dir / 'report.txt'}")