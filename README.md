# Server Log Analyzer

A Python-based log analysis tool that parses server access logs, extracts useful statistics, identifies errors, and generates visual reports in PDF format.

## Overview

The Server Log Analyzer automates the process of analyzing server access logs to provide insights into HTTP requests, server errors, endpoint activity, client traffic, and response sizes.

It processes log entries, calculates statistics, generates charts using Matplotlib, and produces a structured PDF report using ReportLab.

## Features

- **Log Parsing** – Reads and processes server access logs using regular expressions.
- **HTTP Status Analysis** – Tracks HTTP status codes and summarizes successful requests, client errors (4xx), and server errors (5xx).
- **HTTP Method Analysis** – Identifies and counts HTTP methods such as GET, POST, and others.
- **Endpoint Analysis** – Identifies the most frequently requested endpoints and endpoints with errors.
- **IP Address Tracking** – Counts requests per IP address and identifies unique IP addresses.
- **Traffic Analysis** – Tracks the number of requests received per hour.
- **Response Size Analysis** – Calculates average response size and identifies the largest response.
- **Data Visualization** – Generates charts for HTTP status distribution, frequently requested endpoints, and hourly traffic.
- **PDF Report Generation** – Creates a structured PDF report containing summaries, tables, and visualizations.

## Technologies Used

- **Python** – Core programming language
- **Regular Expressions (re)** – Log parsing
- **Collections (Counter)** – Counting and organizing statistics
- **Matplotlib** – Data visualization
- **ReportLab** – PDF report generation
- **Datetime** – Date and time processing

## Project Structure

```text
server-log-analyzer/
│
├── components/
│   ├── __init__.py
│   ├── log_reader.py
│   ├── log_analyzer.py
│   ├── report_generator.py
│   └── report_saver.py
│
├── logs/
│   └── access.log
│
├── reports/
│   └── server_analysis.pdf
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/server-log-analyzer.git
```

### 2. Navigate to the project directory

```bash
cd server-log-analyzer
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Place your server access log file inside the `logs/` directory.
2. Make sure the input filename matches the path configured in `main.py`.
3. Run the application:

```bash
python main.py
```

4. Once processing is complete, the generated PDF report will be saved inside the `reports/` directory.

## Sample Output

The generated PDF report includes the following sections:

1. **Analysis Overview** – Total log entries, unique IP addresses, success rate, and error rate.
2. **HTTP Status Summary** – Distribution of HTTP response status codes.
3. **HTTP Method Summary** – Most frequently used HTTP methods.
4. **Endpoint and Error Analysis** – Frequently requested endpoints and error-producing endpoints.
5. **Traffic and Response Analysis** – Active IP addresses, requests per hour, and response size statistics.

## Dependencies

The project uses the following Python libraries:

```text
matplotlib
reportlab
```

Install them individually using:

```bash
pip install matplotlib reportlab
```

## Author

**Daniel Tababa**

GitHub: [dan123-byte](https://github.com/dan123-byte)

---
