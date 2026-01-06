# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4

# def generate_pdf_report(insights):
#     path = "finance_executive_summary.pdf"

#     doc = SimpleDocTemplate(path, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = []

#     elements.append(Paragraph("Finance AI Agent – Executive Summary", styles["Title"]))
#     elements.append(Spacer(1, 12))

#     for k, v in insights.items():
#         elements.append(Paragraph(f"<b>{k}</b>", styles["Heading2"]))
#         elements.append(Paragraph(v.replace("\n", "<br/>"), styles["BodyText"]))
#         elements.append(Spacer(1, 12))

#     doc.build(elements)
#     return path


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
