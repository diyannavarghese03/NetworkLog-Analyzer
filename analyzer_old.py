from parser import read_logs, parse_logs
import sys
from collections import Counter

if len(sys.argv) > 1:
    LOG_FILE = sys.argv[1]
else:
    LOG_FILE = "logs/sample.log"

logs = read_logs(LOG_FILE)
parsed_logs = parse_logs(logs)

protocol_counter = Counter()
action_counter = Counter()
denied_ips = Counter()
source_ip_counter = Counter()
destination_ip_counter = Counter()

for log in parsed_logs:

    source_ip = log["source_ip"]
    destination_ip = log["destination_ip"]
    protocol = log["protocol"]
    port = log["port"]
    action = log["action"]

    protocol_counter[protocol] += 1
    action_counter[action] += 1
    source_ip_counter[source_ip] += 1
    destination_ip_counter[destination_ip] += 1

    if action == "DENY":
        denied_ips[source_ip] += 1


print("=" * 40)
print("NETWORK LOG ANALYZER")
print("=" * 40)

print(f"\nTotal log entries: {len(logs)}")

print("\nProtocol Statistics")
for protocol, count in protocol_counter.items():
    print(f"  {protocol}: {count}")

print("\nAction Statistics")
for action, count in action_counter.items():
    print(f"  {action}: {count}")

print(f"\nMost common source IP: {source_ip_counter.most_common(1)[0][0]}")

print(f"Most common destination IP: {destination_ip_counter.most_common(1)[0][0]}")
print("\nTop Source IPs")
for ip, count in source_ip_counter.most_common(3):
    print(f"  {ip}: {count}")

print("\nTop Destination IPs")
for ip, count in destination_ip_counter.most_common(3):
    print(f"  {ip}: {count}")

print("\nAnalysis completed successfully.")

def create_report(filename):
    with open(filename, "w") as report:
        report.write("NETWORK LOG ANALYSIS REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Total log entries: {len(logs)}\n\n")

        report.write("Protocol Statistics\n")
        for protocol, count in protocol_counter.items():
            report.write(f"{protocol}: {count}\n")

        report.write("\nAction Statistics\n")
        for action, count in action_counter.items():
            report.write(f"{action}: {count}\n")

        report.write(
            f"\nMost common source IP: {source_ip_counter.most_common(1)[0][0]}\n"
        )

        report.write(
            f"Most common destination IP: {destination_ip_counter.most_common(1)[0][0]}\n"
        )

create_report("reports/report.txt")

print("\nReport saved to reports/report.txt")

print("\nSuspicious Activity")

found = False

for ip, count in denied_ips.items():
    if count >= 3:
        print(f"WARNING: {ip} has {count} denied connections.")
        found = True

if not found:
    print("No suspicious activity detected.")