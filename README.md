# Server Log Analyzer

A Python-based server log analysis application that parses server access logs, extracts useful statistics, identifies potential server errors, and automatically generates downloadable PDF reports containing analysis summaries and visualizations.

## Overview

The Server Log Analyzer automates the process of analyzing server access logs and generating structured PDF reports.

Users can upload multiple log files or select an existing log file from the project directory. Once a file is selected, the application processes its contents, analyzes HTTP requests, tracks traffic patterns, identifies frequently requested and error-producing endpoints, and examines response sizes.

After the analysis is completed, the application automatically generates and downloads a PDF report containing statistical summaries, tables, and visualizations.

The application provides a simple Streamlit interface for importing log files and generating reports without manually executing the analysis scripts.

## Features

- **Log File Upload** – Upload multiple server access log files in `.log` or `.txt` format.
- **Multiple File Support** – Import and choose between multiple uploaded log files.
- **Existing Log File Selection** – Select the existing `logs/access.log` file if available.
- **Log Parsing** – Reads and processes server access logs using regular expressions.
- **HTTP Status Analysis** – Tracks HTTP status codes and summarizes successful requests, client errors (4xx), and server errors (5xx).
- **HTTP Method Analysis** – Identifies and counts HTTP methods such as GET, POST, and others.
- **Endpoint Analysis** – Identifies the most frequently requested endpoints and endpoints associated with errors.
- **Error Endpoint Analysis** – Separately identifies endpoints generating client errors (4xx) and server errors (5xx).
- **IP Address Tracking** – Counts requests per IP address and identifies unique IP addresses.
- **Traffic Analysis** – Tracks the number of requests received per hour and identifies the busiest hour.
- **Response Size Analysis** – Calculates average response size and identifies the largest response and its endpoint.
- **Automated PDF Report Generation** – Generates structured PDF reports containing analysis summaries, statistical tables, and visualizations.
- **Automatic PDF Download** – Automatically downloads the generated PDF report after successful analysis.
- **Temporary File Handling** – Uses temporary files and directories to process uploaded logs and generate reports without permanently storing intermediate files.

## Application Workflow

1. **Import Log Files** – Upload one or more `.log` or `.txt` files through the Streamlit file uploader.
2. **Select Log File** – Choose an uploaded file or the existing `logs/access.log` file.
3. **Generate Report** – Click the **Generate & Download Report** button to start processing.
4. **Parse Log Entries** – The application reads and extracts valid entries from the selected log file.
5. **Analyze Server Activity** – Processes the log entries and calculates relevant server statistics.
6. **Generate PDF** – Creates a structured PDF report containing the analysis results and visualizations.
7. **Download Report** – Automatically downloads the generated `server_analysis.pdf` file.

## Analysis Metrics

The application analyzes the following server log information:

### HTTP Status Analysis

- HTTP status code distribution.
- Successful requests (2xx).
- Client errors (4xx).
- Server errors (5xx).

### HTTP Method Analysis

- Request counts by HTTP method.
- Most frequently used HTTP method.

### Endpoint Analysis

- Most frequently requested endpoints.
- Endpoints associated with client errors (4xx).
- Endpoints associated with server errors (5xx).
- Request success and error statistics.

### IP Address Analysis

- Total unique IP addresses.
- Number of requests per IP address.

### Traffic Analysis

- Number of requests received per hour.
- Busiest hour based on request volume.

### Response Size Analysis

- Average response size.
- Largest response size.
- Endpoint associated with the largest response.

## Technologies Used

- **Python** – Core programming language.
- **Streamlit** – Web application interface and file upload functionality.
- **Pandas** – Data organization and tabular data processing.
- **Plotly Express** – Data visualization.
- **Regular Expressions (re)** – Server log parsing.
- **Collections (Counter)** – Counting and organizing statistics.
- **Matplotlib** – PDF report visualizations.
- **ReportLab** – PDF report generation.
- **Datetime** – Date and time processing.
- **Base64** – Encodes generated PDF files for automatic browser downloading.
- **Tempfile** – Handles temporary log files and report generation.

## Project Structure

```text
server-log-analyzer/
│
├── components/
│   ├── __init__.py
│   ├── log_parser.py
│   ├── log_analyzer.py
│   └── report_generator.py
│
├── logs/
│   └── access.log
│
├── reports/
│
├── app.py
├── main.py
├── style.css
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/dan123-byte/server-log-analyzer.git
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

### 1. Start the application

```bash
python -m streamlit run app.py
```

### 2. Open the application

Streamlit will launch the application in your default browser.

### 3. Import a log file

- Upload one or more `.log` or `.txt` files using the file uploader.
- Alternatively, select the existing `logs/access.log` file if available.

### 4. Select a log file

Choose your preferred log file from the **Select Log File** dropdown.

### 5. Generate and download the report

Click the **Generate & Download Report** button.

The application will automatically:

- Read and parse the selected log file.
- Analyze server activity and calculate statistics.
- Generate a PDF report.
- Initiate the PDF download in your browser.

The generated report will be downloaded as:

```text
server_analysis.pdf
```

## Sample Output

The application generates a PDF report containing:

- Server log analysis overview.
- HTTP status code statistics.
- HTTP method distribution.
- Frequently requested endpoints.
- Client and server error endpoint summaries.
- IP address statistics.
- Hourly traffic analysis.
- Response size statistics.
- Statistical tables and visualizations.

## Dependencies

The project uses the following Python libraries:

```text
streamlit
pandas
plotly
matplotlib
reportlab
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## Author

**Daniel Tababa**

GitHub: [dan123-byte](https://github.com/dan123-byte)

---
