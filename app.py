import os
import tempfile
import base64
import streamlit as st
import streamlit.components.v1 as components

from components.log_parser import read_logs
from components.log_analyzer import analyze_logs
from components.report_generator import generate_report


st.set_page_config(
    page_title="Server Log Analyzer",
    page_icon="📊",
    layout="wide"
)


def load_css(file_path):

    with open(file_path, "r") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )

load_css("style.css")

st.title("Server Log Analyzer")

st.caption(
    "Import a server log file, analyze server activity, "
    "and automatically download the PDF report."
)

st.divider()

uploaded_files = st.file_uploader(
    "Import Log Files",
    type=["log", "txt"],
    accept_multiple_files=True,
    help="Import one or more server log files."
)


log_options = {}

if os.path.exists("logs/access.log"):
    log_options["access.log"] = "logs/access.log"


if uploaded_files:

    for index, uploaded_file in enumerate(uploaded_files):

        option_name = uploaded_file.name

        if option_name in log_options:
            option_name = f"{uploaded_file.name} ({index + 1})"

        log_options[option_name] = uploaded_file


if not log_options:

    st.info("Import a log file to get started.")
    st.stop()

selected_log = st.selectbox(
    "Select Log File",
    options=list(log_options.keys())
)

if st.button(
    "📥 Generate & Download Report",
    type="primary",
    use_container_width=True
):

    selected_source = log_options[selected_log]

    try:

        with st.spinner("Generating your PDF report..."):

            # Read log file
            if isinstance(selected_source, str):

                logs = list(read_logs(selected_source))

            else:

                with tempfile.NamedTemporaryFile(
                    mode="wb",
                    suffix=".log",
                    delete=False
                ) as temp_file:

                    temp_file.write(selected_source.getvalue())
                    temp_path = temp_file.name

                try:
                    logs = list(read_logs(temp_path))

                finally:
                    os.remove(temp_path)

            if not logs:

                st.warning("No valid log entries found.")
                st.stop()

            stats = analyze_logs(logs)

            with tempfile.TemporaryDirectory() as temp_dir:

                pdf_path = os.path.join(
                    temp_dir,
                    "server_analysis.pdf"
                )

                generate_report(stats, pdf_path)

                with open(pdf_path, "rb") as report:
                    pdf_data = report.read()

        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")

        download_html = f"""
        <html>
            <body>
                <script>
                    const link = document.createElement("a");

                    link.href = "data:application/pdf;base64,{pdf_base64}";
                    link.download = "server_analysis.pdf";

                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                </script>
            </body>
        </html>
        """

        components.html(
            download_html,
            height=0,
            scrolling=False
        )

        st.success("PDF report generated successfully!")

    except FileNotFoundError as error:

        st.error(str(error))

    except Exception as error:

        st.error(f"Unable to generate report: {error}")

st.divider()

st.caption(
    "Server Log Analyzer | PDF Report Generator"
)
