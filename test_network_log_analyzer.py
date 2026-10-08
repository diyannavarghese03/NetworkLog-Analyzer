from pathlib import Path

from report import print_report, save_report


def test_print_report_handles_empty_results(capsys):
    empty_results = {
        "total_logs": 0,
        "protocol_counter": {},
        "action_counter": {},
        "source_ip_counter": {},
        "destination_ip_counter": {},
        "denied_ips": {},
    }

    print_report(empty_results)
    captured = capsys.readouterr()

    assert "Total log entries: 0" in captured.out
    assert "No data available" in captured.out


def test_save_report_handles_empty_results(tmp_path):
    output_path = tmp_path / "report.txt"
    empty_results = {
        "total_logs": 0,
        "protocol_counter": {},
        "action_counter": {},
        "source_ip_counter": {},
        "destination_ip_counter": {},
        "denied_ips": {},
    }

    save_report(empty_results, str(output_path))

    content = output_path.read_text(encoding="utf-8")
    assert "Total log entries: 0" in content
    assert "No data available" in content
