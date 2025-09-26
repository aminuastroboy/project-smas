from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_student_report(student, result_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(width/2, height-50, f"{student.user.get_full_name()} - Exam Report")
    c.setFont('Helvetica', 12)
    c.drawString(50, height-100, f"Exam: {result_data.get('exam')}")
    c.drawString(50, height-120, f"Score: {result_data.get('total_score')}")
    c.drawString(50, height-140, f"Percentage: {round(result_data.get('percentage',0),1)}%")
    y = height-180
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, 'Performance by Topic:')
    y -= 18
    c.setFont('Helvetica', 11)
    breakdown = result_data.get('breakdown', {})
    if isinstance(breakdown, dict):
        for topic, percent in breakdown.items():
            c.drawString(70, y, f"{topic}: {percent}%")
            y -= 16
            if y < 80:
                c.showPage(); y = height-80
    y -= 10
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, 'Weak Topics:')
    y -= 18
    c.setFont('Helvetica', 11)
    for t in result_data.get('weak_topics', []):
        c.drawString(70, y, f"- {t}")
        y -= 16
        if y < 80:
            c.showPage(); y = height-80
    y -= 10
    c.setFont('Helvetica-Bold',12)
    c.drawString(50, y, 'Career Advice:')
    y -= 18
    c.setFont('Helvetica',11)
    for ad in result_data.get('career_advice', []):
        c.drawString(70, y, f"- {ad}")
        y -= 16
        if y < 80:
            c.showPage(); y = height-80
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
