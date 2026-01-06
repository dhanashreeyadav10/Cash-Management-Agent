from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(insights):
    path = "finance_report.pdf"
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)

    elements = [Paragraph("Finance AI Report", styles["Title"])]

    for k, v in insights.items():
        elements.append(Paragraph(f"<b>{k}</b><br/>{v}", styles["BodyText"]))

    doc.build(elements)
    return path
