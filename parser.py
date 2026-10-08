def read_logs(filename):
    """Read all log lines from a file."""
    with open(filename, "r") as file:
        return file.readlines()


def parse_logs(logs):
    """
    Parse log lines into dictionaries.
    Skip invalid log entries.
    """

    parsed_logs = []

    for line in logs:
        parts = line.strip().split()

        if len(parts) != 6:
            print(f"Skipping invalid log: {line.strip()}")
            continue

        parsed_logs.append({
            "source_ip": parts[0],
            "destination_ip": parts[2],
            "protocol": parts[3],
            "port": parts[4],
            "action": parts[5]
        })

    return parsed_logs