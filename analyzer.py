from collections import Counter


def analyze_logs(parsed_logs):

    protocol_counter = Counter()
    action_counter = Counter()
    source_ip_counter = Counter()
    destination_ip_counter = Counter()
    denied_ips = Counter()

    for log in parsed_logs:

        protocol_counter[log["protocol"]] += 1
        action_counter[log["action"]] += 1
        source_ip_counter[log["source_ip"]] += 1
        destination_ip_counter[log["destination_ip"]] += 1

        if log["action"] == "DENY":
            denied_ips[log["source_ip"]] += 1

    return {
        "total_logs": len(parsed_logs),
        "protocol_counter": protocol_counter,
        "action_counter": action_counter,
        "source_ip_counter": source_ip_counter,
        "destination_ip_counter": destination_ip_counter,
        "denied_ips": denied_ips
    }