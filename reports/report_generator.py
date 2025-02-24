# reports/report_generator.py
import pdfkit
from jinja2 import Template
import os

def generate_report(llm_summary, dcf_data, consolidation_data, budget_data, forecast_data, risk_analysis):
    """
    Combine data into an HTML template, then convert to PDF via pdfkit.
    """
    template_str = """
    <html>
    <head>
      <title>Final Financial Report</title>
      <style>
        body { font-family: Arial, sans-serif; }
        table, th, td {
          border: 1px solid #ccc;
          border-collapse: collapse;
          padding: 5px;
        }
        h1, h2 { color: #333; }
      </style>
    </head>
    <body>
      <h1>Comprehensive Financial Report</h1>
      <h2>LLM Summary</h2>
      <p>{{ llm_summary }}</p>

      <h2>DCF Results</h2>
      <pre>{{ dcf_data }}</pre>

      <h2>Consolidation Results</h2>
      <pre>{{ consolidation_data }}</pre>

      <h2>Budget Results</h2>
      <pre>{{ budget_data }}</pre>

      <h2>Forecast Results</h2>
      <pre>{{ forecast_data }}</pre>

      <h2>Risk Analysis</h2>
      <pre>{{ risk_analysis }}</pre>
    </body>
    </html>
    """
    template = Template(template_str)
    filled_html = template.render(
        llm_summary=llm_summary,
        dcf_data=dcf_data,
        consolidation_data=consolidation_data,
        budget_data=budget_data,
        forecast_data=forecast_data,
        risk_analysis=risk_analysis
    )

    output_pdf = "final_report.pdf"
    pdfkit.from_string(filled_html, output_pdf)
    return output_pdf
