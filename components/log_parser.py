import re
from datetime import datetime

LOG_PATTERN = (
    r'(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) '
    r'(?P<endpoint>\S+) '
    r'(?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) '
    r'(?P<size>\S+)'
)


def parse_log_line(line):

    match = re.search(LOG_PATTERN, line)

    if not match:
        return None

    data = match.groupdict()

    try:
        timestamp = datetime.strptime(
            data["timestamp"],
            "%d/%b/%Y:%H:%M:%S %z"
        )
    except ValueError:
        timestamp = None

    response_size = (
        int(data["size"])
        if data["size"].isdigit()
        else None
    )

    return {
        "ip": data["ip"],
        "timestamp": timestamp,
        "method": data["method"],
        "endpoint": data["endpoint"],
        "protocol": data["protocol"],
        "status": data["status"],
        "size": response_size
    }


def read_logs(file_path):

    try:

        with open(file_path, "r") as file:

            for line in file:

                log = parse_log_line(line)

                if log is not None:
                    yield log

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Log file not found: {file_path}"
        )