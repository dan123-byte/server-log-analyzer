from components import (
    read_logs,
    analyze_logs,
    generate_report,
)

def main():

    try:

        logs = read_logs("logs/access.log")

        stats = analyze_logs(logs)

        generate_report(stats, "reports/server_analysis.pdf")

    except FileNotFoundError as error:

        print("Error:", error)

if __name__ == "__main__":
    main()
