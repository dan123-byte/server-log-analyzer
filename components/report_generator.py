import os

def generate_report(stats):

    report = ""

    report += "================================\n"
    report += "       SERVER LOG ANALYZER\n"
    report += "================================\n"

    report += f"\nTotal Log Entries: {stats['total_logs']}\n"

    report += "\nHTTP STATUS SUMMARY\n"

    for code, total in stats["status_codes"].most_common():
        report += f"{code} : {total}\n"

    report += "\nHTTP METHOD SUMMARY\n"

    for method, total in stats["methods"].most_common():
        report += f"{method} : {total}\n"

    report += f"\nMost Used HTTP Method: {stats['most_used_method']}\n"

    report += "\nERROR SUMMARY\n"
    report += f"Client Errors (4xx): {stats['client_errors']}\n"
    report += f"Server Errors (5xx): {stats['server_errors']}\n"

    report += "\nFREQUENT ERRORS\n"

    for code, total in stats["status_codes"].most_common():

        if code.startswith(("4", "5")):
            report += f"{code} : {total}\n"

    report += "\nREQUEST SUCCESS AND ERROR RATES\n"

    report += f"Successful Requests (2xx): {stats['success_percentage']:.2f}%\n"
    report += f"Error Requests (4xx and 5xx): {stats['error_percentage']:.2f}%\n"

    report += "\nTOP 5 REQUESTED ENDPOINTS\n"

    for endpoint, total in stats["endpoints"].most_common(5):
        report += f"{endpoint} : {total} requests\n"

    report += "\nTOP 5 ERROR ENDPOINTS\n"

    for endpoint, total in stats["error_endpoints"].most_common(5):
        report += f"{endpoint} : {total} errors\n"

    report += "\nTOP 5 CLIENT ERROR ENDPOINTS (4xx)\n"

    for endpoint, total in stats["client_error_endpoints"].most_common(5):
        report += f"{endpoint} : {total} errors\n"

    report += "\nTOP 5 SERVER ERROR ENDPOINTS (5xx)\n"

    for endpoint, total in stats["server_error_endpoints"].most_common(5):
        report += f"{endpoint} : {total} errors\n"

    report += "\nTOP 5 ACTIVE IP ADDRESSES\n"

    for ip, total in stats["ip_addresses"].most_common(5):
        report += f"{ip} : {total} requests\n"

    report += f"\nUnique IP Addresses: {len(stats['unique_ips'])}\n"

    report += "\nREQUESTS PER HOUR\n"

    for hour, total in stats["requests_per_hour"].most_common():
        report += f"{hour} : {total} requests\n"

    if stats["requests_per_hour"]:

        busiest_hour, busiest_count = (
            stats["requests_per_hour"].most_common(1)[0]
        )

        report += f"\nBusiest Hour: {busiest_hour} ({busiest_count} requests)\n"

    report += "\nRESPONSE SIZE STATISTICS\n"

    report += f"Average Response Size: {stats['average_response_size']:.2f} bytes\n"
    report += f"Largest Response Size: {stats['largest_response']} bytes\n"
    report += f"Largest Response Endpoint: {stats['largest_response_endpoint']}\n"

    report += f"\nResponses With Recorded Sizes: {stats['response_count']}\n"

    report += "\n================================\n"
    report += "       ANALYSIS COMPLETE\n"
    report += "================================\n"

    return report

def save_report(report, file_path):

    try:

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            file.write(report)

        print(f"Report saved successfully to {file_path}")

    except OSError as error:
        print("Error saving report:", error)