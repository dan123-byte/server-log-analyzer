from collections import Counter

def analyze_logs(logs):

    count = 0

    status_codes = Counter()
    endpoints = Counter()
    error_endpoints = Counter()
    client_error_endpoints = Counter()
    server_error_endpoints = Counter()
    methods = Counter()
    ip_addresses = Counter()
    requests_per_hour = Counter()

    unique_ips = set()

    client_errors = 0
    server_errors = 0
    successful_requests = 0

    total_response_size = 0
    response_count = 0
    largest_response = 0
    largest_response_endpoint = "N/A"

    for log in logs:

        count += 1

        ip = log["ip"]
        timestamp = log["timestamp"]
        endpoint = log["endpoint"]
        status = log["status"]
        method = log["method"]
        size = log["size"]

        status_codes[status] += 1

        endpoints[endpoint] += 1

        methods[method] += 1

        ip_addresses[ip] += 1
        unique_ips.add(ip)

        if status.startswith("2"):
            successful_requests += 1

        if status.startswith("4"):

            client_errors += 1
            client_error_endpoints[endpoint] += 1

        elif status.startswith("5"):

            server_errors += 1
            server_error_endpoints[endpoint] += 1

        if status.startswith(("4", "5")):
            error_endpoints[endpoint] += 1

        if timestamp is not None:

            hour = timestamp.strftime("%H:00")
            requests_per_hour[hour] += 1

        if size is not None:

            total_response_size += size
            response_count += 1

            if size > largest_response:

                largest_response = size
                largest_response_endpoint = endpoint

    error_percentage = (
        ((client_errors + server_errors) / count) * 100
        if count else 0
    )

    success_percentage = (
        (successful_requests / count) * 100
        if count else 0
    )

    average_response_size = (
        total_response_size / response_count
        if response_count else 0
    )

    most_used_method = (
        methods.most_common(1)[0][0]
        if methods else "N/A"
    )

    return {

        "total_logs": count,

        "status_codes": status_codes,
        "endpoints": endpoints,
        "error_endpoints": error_endpoints,
        "client_error_endpoints": client_error_endpoints,
        "server_error_endpoints": server_error_endpoints,

        "methods": methods,
        "ip_addresses": ip_addresses,
        "unique_ips": unique_ips,
        "requests_per_hour": requests_per_hour,

        "client_errors": client_errors,
        "server_errors": server_errors,
        "successful_requests": successful_requests,

        "error_percentage": error_percentage,
        "success_percentage": success_percentage,

        "average_response_size": average_response_size,
        "largest_response": largest_response,
        "largest_response_endpoint": largest_response_endpoint,
        "response_count": response_count,

        "most_used_method": most_used_method
    }
