import os
from io import BytesIO
from html import escape
from datetime import datetime

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

NAVY = colors.HexColor("#172554")
BLUE = colors.HexColor("#2563EB")
LIGHT_BLUE = colors.HexColor("#EFF6FF")
LIGHT_GRAY = colors.HexColor("#F1F5F9")
DARK_GRAY = colors.HexColor("#334155")
WHITE = colors.white

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ReportTitle",
    parent=styles["Title"],
    fontSize=23,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=5
))

styles.add(ParagraphStyle(
    name="Subtitle",
    parent=styles["Normal"],
    fontSize=9,
    textColor=DARK_GRAY,
    alignment=TA_CENTER,
    spaceAfter=20
))

styles.add(ParagraphStyle(
    name="SectionHeading",
    parent=styles["Heading2"],
    fontSize=13,
    textColor=NAVY,
    spaceBefore=12,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name="SmallText",
    parent=styles["Normal"],
    fontSize=8,
    leading=11
))

styles.add(ParagraphStyle(
    name="CardLabel",
    parent=styles["Normal"],
    fontSize=8,
    textColor=NAVY,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold"
))

styles.add(ParagraphStyle(
    name="CardValue",
    parent=styles["Normal"],
    fontSize=15,
    textColor=NAVY,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold"
))

def create_chart(labels, values, title, horizontal=False):

    buffer = BytesIO()

    if not labels:
        labels = ["No data"]
        values = [0]

    fig, ax = plt.subplots(figsize=(8, 3.2))

    if horizontal:

        ax.barh(labels[::-1], values[::-1])
        ax.set_xlabel("Requests")
        ax.grid(axis="x", linestyle="--", alpha=0.3)

    else:

        ax.bar(labels, values)
        ax.set_ylabel("Requests")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

    ax.set_title(title, fontsize=13, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    buffer.seek(0)

    return Image(
        buffer,
        width=165 * mm,
        height=65 * mm
    )


def create_table(headers, rows, widths=None):

    table_data = []

    formatted_headers = [
        Paragraph(
            escape(str(header)),
            styles["SmallText"]
        )
        for header in headers
    ]

    table_data.append(formatted_headers)

    for row in rows:

        formatted_row = []

        for cell in row:

            if isinstance(cell, Paragraph):
                formatted_row.append(cell)

            else:
                formatted_row.append(
                    Paragraph(
                        escape(str(cell)),
                        styles["SmallText"]
                    )
                )

        table_data.append(formatted_row)

    table = Table(
        table_data,
        colWidths=widths,
        repeatRows=1
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), NAVY),

        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("FONTSIZE", (0, 0), (-1, -1), 8),

        ("LEADING", (0, 0), (-1, -1), 11),

        ("GRID", (0, 0), (-1, -1), 0.4,
         colors.HexColor("#CBD5E1")),

        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [WHITE, LIGHT_GRAY]),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("LEFTPADDING", (0, 0), (-1, -1), 7),

        ("RIGHTPADDING", (0, 0), (-1, -1), 7),

        ("TOPPADDING", (0, 0), (-1, -1), 7),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),

    ]))

    return table

def create_summary_cards(stats):

    cards = [

        [
            Paragraph("TOTAL LOGS", styles["CardLabel"]),
            Paragraph(
                str(stats["total_logs"]),
                styles["CardValue"]
            )
        ],

        [
            Paragraph("UNIQUE IPs", styles["CardLabel"]),
            Paragraph(
                str(len(stats["unique_ips"])),
                styles["CardValue"]
            )
        ],

        [
            Paragraph("SUCCESS RATE", styles["CardLabel"]),
            Paragraph(
                f'{stats["success_percentage"]:.2f}%',
                styles["CardValue"]
            )
        ],

        [
            Paragraph("ERROR RATE", styles["CardLabel"]),
            Paragraph(
                f'{stats["error_percentage"]:.2f}%',
                styles["CardValue"]
            )
        ]

    ]

    table = Table(
        [cards],
        colWidths=[42 * mm] * 4
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),

        ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("BOX", (0, 0), (-1, -1), 0.5, BLUE),

        ("INNERGRID", (0, 0), (-1, -1), 0.5, BLUE),

        ("TOPPADDING", (0, 0), (-1, -1), 10),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),

    ]))

    return table

def add_footer(canvas, document):

    canvas.saveState()

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(DARK_GRAY)

    canvas.drawString(
        20 * mm,
        12 * mm,
        "SERVER LOG ANALYZER"
    )

    canvas.drawRightString(
        190 * mm,
        12 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()

def generate_report(stats, file_path="reports/server_analysis.pdf"):

    try:

        os.makedirs(
            os.path.dirname(file_path) or ".",
            exist_ok=True
        )

        document = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=22 * mm
        )

        elements = []

        elements.append(Paragraph(
            "SERVER LOG ANALYZER",
            styles["ReportTitle"]
        ))

        elements.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y %I:%M %p')}",
            styles["Subtitle"]
        ))

        elements.append(Paragraph(
            "ANALYSIS OVERVIEW",
            styles["SectionHeading"]
        ))

        elements.append(create_summary_cards(stats))

        elements.append(Spacer(1, 15))

        elements.append(Paragraph(
            "HTTP STATUS SUMMARY",
            styles["SectionHeading"]
        ))

        status_rows = [
            [str(code), str(total)]
            for code, total in stats["status_codes"].most_common()
        ]

        elements.append(create_table(
            ["HTTP Status", "Total Requests"],
            status_rows,
            [80 * mm, 85 * mm]
        ))

        elements.append(Spacer(1, 10))

        elements.append(create_chart(
            [
                str(code)
                for code, total in stats["status_codes"].most_common()
            ],
            [
                total
                for code, total in stats["status_codes"].most_common()
            ],
            "HTTP Status Distribution"
        ))

        elements.append(Paragraph(
            "HTTP METHOD SUMMARY",
            styles["SectionHeading"]
        ))

        method_rows = [
            [str(method), str(total)]
            for method, total in stats["methods"].most_common()
        ]

        elements.append(create_table(
            ["HTTP Method", "Total Requests"],
            method_rows,
            [80 * mm, 85 * mm]
        ))

        elements.append(Paragraph(
            f'Most Used HTTP Method: {escape(str(stats["most_used_method"]))}',
            styles["SmallText"]
        ))

        elements.append(PageBreak())

        elements.append(Paragraph(
            "ENDPOINT AND ERROR ANALYSIS",
            styles["SectionHeading"]
        ))

        error_rows = [

            ["Client Errors (4xx)", str(stats["client_errors"])],

            ["Server Errors (5xx)", str(stats["server_errors"])]

        ]

        elements.append(create_table(
            ["Error Category", "Total"],
            error_rows,
            [80 * mm, 85 * mm]
        ))

        elements.append(Spacer(1, 10))

        elements.append(Paragraph(
            "REQUEST SUCCESS AND ERROR RATES",
            styles["SectionHeading"]
        ))

        rate_rows = [

            [
                "Successful Requests (2xx)",
                f'{stats["success_percentage"]:.2f}%'
            ],

            [
                "Error Requests (4xx and 5xx)",
                f'{stats["error_percentage"]:.2f}%'
            ]

        ]

        elements.append(create_table(
            ["Request Category", "Percentage"],
            rate_rows,
            [80 * mm, 85 * mm]
        ))

        elements.append(Paragraph(
            "TOP 5 REQUESTED ENDPOINTS",
            styles["SectionHeading"]
        ))

        endpoint_rows = [
            [str(endpoint), str(total)]
            for endpoint, total in stats["endpoints"].most_common(5)
        ]

        elements.append(create_table(
            ["Endpoint", "Requests"],
            endpoint_rows,
            [130 * mm, 35 * mm]
        ))

        elements.append(Spacer(1, 8))

        elements.append(create_chart(
            [
                str(endpoint)
                for endpoint, total in stats["endpoints"].most_common(5)
            ],
            [
                total
                for endpoint, total in stats["endpoints"].most_common(5)
            ],
            "Top 5 Requested Endpoints",
            horizontal=True
        ))

        elements.append(Paragraph(
            "TOP 5 ERROR ENDPOINTS",
            styles["SectionHeading"]
        ))

        error_endpoint_rows = [
            [str(endpoint), str(total)]
            for endpoint, total in stats["error_endpoints"].most_common(5)
        ]

        elements.append(create_table(
            ["Endpoint", "Errors"],
            error_endpoint_rows,
            [130 * mm, 35 * mm]
        ))

        elements.append(Paragraph(
            "TOP 5 CLIENT ERROR ENDPOINTS (4xx)",
            styles["SectionHeading"]
        ))

        client_rows = [
            [str(endpoint), str(total)]
            for endpoint, total in stats["client_error_endpoints"].most_common(5)
        ]

        elements.append(create_table(
            ["Endpoint", "Errors"],
            client_rows,
            [130 * mm, 35 * mm]
        ))

        elements.append(Paragraph(
            "TOP 5 SERVER ERROR ENDPOINTS (5xx)",
            styles["SectionHeading"]
        ))

        server_rows = [
            [str(endpoint), str(total)]
            for endpoint, total in stats["server_error_endpoints"].most_common(5)
        ]

        elements.append(create_table(
            ["Endpoint", "Errors"],
            server_rows,
            [130 * mm, 35 * mm]
        ))

        elements.append(PageBreak())

        elements.append(Paragraph(
            "TRAFFIC AND RESPONSE ANALYSIS",
            styles["SectionHeading"]
        ))

        elements.append(Paragraph(
            "TOP 5 ACTIVE IP ADDRESSES",
            styles["SectionHeading"]
        ))

        ip_rows = [
            [str(ip), str(total)]
            for ip, total in stats["ip_addresses"].most_common(5)
        ]

        elements.append(create_table(
            ["IP Address", "Requests"],
            ip_rows,
            [80 * mm, 85 * mm]
        ))

        elements.append(Paragraph(
            f'Unique IP Addresses: {len(stats["unique_ips"])}',
            styles["SmallText"]
        ))

        elements.append(Paragraph(
            "REQUESTS PER HOUR",
            styles["SectionHeading"]
        ))

        hourly_data = sorted(
            stats["requests_per_hour"].items()
        )

        hourly_rows = [
            [str(hour), str(total)]
            for hour, total in hourly_data
        ]

        elements.append(create_table(
            ["Hour", "Requests"],
            hourly_rows,
            [80 * mm, 85 * mm]
        ))

        if hourly_data:

            busiest_hour, busiest_count = max(
                hourly_data,
                key=lambda item: item[1]
            )

            elements.append(Paragraph(
                f"Busiest Hour: {escape(str(busiest_hour))} "
                f"({busiest_count} requests)",
                styles["SmallText"]
            ))

        elements.append(Spacer(1, 10))

        elements.append(create_chart(
            [
                str(hour)
                for hour, total in hourly_data
            ],
            [
                total
                for hour, total in hourly_data
            ],
            "Requests Per Hour"
        ))

        elements.append(Paragraph(
            "RESPONSE SIZE STATISTICS",
            styles["SectionHeading"]
        ))

        response_rows = [

            [
                "Average Response Size",
                f'{stats["average_response_size"]:.2f} bytes'
            ],

            [
                "Largest Response Size",
                f'{stats["largest_response"]} bytes'
            ],

            [
                "Largest Response Endpoint",
                str(stats["largest_response_endpoint"])
            ],

            [
                "Responses With Recorded Sizes",
                str(stats["response_count"])
            ]

        ]

        elements.append(create_table(
            ["Metric", "Value"],
            response_rows,
            [80 * mm, 85 * mm]
        ))

        document.build(
            elements,
            onFirstPage=add_footer,
            onLaterPages=add_footer
        )

        print(
            f"PDF report generated successfully: {file_path}"
        )

    except (OSError, ValueError, KeyError, TypeError) as error:

        print(
            "Error generating PDF report:",
            error
        )