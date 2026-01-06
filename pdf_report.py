
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(insights):
    path = "finance_report.pdf"
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    elements = [Paragraph("Finance AI Report", styles["Title"])]
    for k, v in insights.items():
        elements.append(Paragraph(f"<b>{k}</b>: {v}", styles["BodyText"]))

    doc.build(elements)
    return path

