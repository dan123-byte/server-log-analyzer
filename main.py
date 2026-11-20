from components import (
    read_logs,
    analyze_logs,
    generate_report,
    save_report
)

def main():

    try:

        logs = read_logs("logs/access.log")

        stats = analyze_logs(logs)

        report = generate_report(stats)

        print(report)

        save_report(report, "reports/summary.txt")

    except FileNotFoundError as error:

        print("Error:", error)


if __name__ == "__main__":
    main()
