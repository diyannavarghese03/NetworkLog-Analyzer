from collections import Counter
from pathlib import Path


def _normalize_counter(counter):
    """Accept either Counter objects or plain dictionaries."""
    if counter is None:
        return Counter()
    if isinstance(counter, Counter):
        return counter
    return Counter(counter)


def _most_common_value(counter, limit=1):
    """Return the most common item or a friendly fallback."""
    normalized = _normalize_counter(counter)
    if not normalized:
        return None
    return normalized.most_common(limit)


def print_report(results):
    """Print analysis results to the terminal."""
    protocol_counter = _normalize_counter(results.get("protocol_counter", {}))
    action_counter = _normalize_counter(results.get("action_counter", {}))
    source_ip_counter = _normalize_counter(results.get("source_ip_counter", {}))
    destination_ip_counter = _normalize_counter(results.get("destination_ip_counter", {}))
    denied_ips = _normalize_counter(results.get("denied_ips", {}))

    print("=" * 40)
    print("NETWORK LOG ANALYZER")
    print("=" * 40)

    print(f"\nTotal log entries: {results.get('total_logs', 0)}")

    print("\nProtocol Statistics")
    if protocol_counter:
        for protocol, count in protocol_counter.items():
            print(f"  {protocol}: {count}")
    else:
        print("  No data available.")

    print("\nAction Statistics")
    if action_counter:
        for action, count in action_counter.items():
            print(f"  {action}: {count}")
    else:
        print("  No data available.")

    most_common_source = _most_common_value(source_ip_counter, 1)
    print(
        f"\nMost common source IP: "
        f"{most_common_source[0][0] if most_common_source else 'N/A'}"
    )

    most_common_destination = _most_common_value(destination_ip_counter, 1)
    print(
        f"Most common destination IP: "
        f"{most_common_destination[0][0] if most_common_destination else 'N/A'}"
    )

    print("\nTop Source IPs")
    if source_ip_counter:
        for ip, count in source_ip_counter.most_common(3):
            print(f"  {ip}: {count}")
    else:
        print("  No data available.")

    print("\nTop Destination IPs")
    if destination_ip_counter:
        for ip, count in destination_ip_counter.most_common(3):
            print(f"  {ip}: {count}")
    else:
        print("  No data available.")

    print("\nSuspicious Activity")
    found = False

    for ip, count in denied_ips.items():
        if count >= 3:
            print(f"WARNING: {ip} has {count} denied connections.")
            found = True

    if not found:
        print("No suspicious activity detected.")

    print("\nAnalysis completed successfully.")


def save_report(results, filename):
    """Save analysis results to a text file."""
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    protocol_counter = _normalize_counter(results.get("protocol_counter", {}))
    action_counter = _normalize_counter(results.get("action_counter", {}))
    source_ip_counter = _normalize_counter(results.get("source_ip_counter", {}))
    destination_ip_counter = _normalize_counter(results.get("destination_ip_counter", {}))
    denied_ips = _normalize_counter(results.get("denied_ips", {}))

    with output_path.open("w", encoding="utf-8") as report:
        report.write("NETWORK LOG ANALYSIS REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Total log entries: {results.get('total_logs', 0)}\n\n")

        report.write("Protocol Statistics\n")
        if protocol_counter:
            for protocol, count in protocol_counter.items():
                report.write(f"{protocol}: {count}\n")
        else:
            report.write("No data available.\n")

        report.write("\nAction Statistics\n")
        if action_counter:
            for action, count in action_counter.items():
                report.write(f"{action}: {count}\n")
        else:
            report.write("No data available.\n")

        most_common_source = _most_common_value(source_ip_counter, 1)
        report.write(
            f"\nMost common source IP: "
            f"{most_common_source[0][0] if most_common_source else 'N/A'}\n"
        )

        most_common_destination = _most_common_value(destination_ip_counter, 1)
        report.write(
            f"Most common destination IP: "
            f"{most_common_destination[0][0] if most_common_destination else 'N/A'}\n"
        )

        report.write("\nTop Source IPs\n")
        if source_ip_counter:
            for ip, count in source_ip_counter.most_common(3):
                report.write(f"{ip}: {count}\n")
        else:
            report.write("No data available.\n")

        report.write("\nTop Destination IPs\n")
        if destination_ip_counter:
            for ip, count in destination_ip_counter.most_common(3):
                report.write(f"{ip}: {count}\n")
        else:
            report.write("No data available.\n")

        report.write("\nSuspicious Activity\n")
        found = False
        for ip, count in denied_ips.items():
            if count >= 3:
                report.write(f"WARNING: {ip} has {count} denied connections.\n")
                found = True

        if not found:
            report.write("No suspicious activity detected.\n")

        report.write("\nAnalysis completed successfully.\n")