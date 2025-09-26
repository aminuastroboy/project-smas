from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_class_report(analytics_data, class_name='Class Report'):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(width/2, height-50, f"{class_name} - Performance Report")
    y = height-100
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, 'Average Scores Per Exam:')
    y -= 20
    c.setFont('Helvetica', 11)
    for item in analytics_data.get('average_scores', []):
        c.drawString(70, y, f"{item['exam']}: {item['avg']}%")
        y -= 18
    y -= 10
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, 'Weak Topics Across Class:')
    y -= 20
    c.setFont('Helvetica', 11)
    for topic, count in analytics_data.get('weak_topics', {}).items():
        c.drawString(70, y, f"{topic}: {count} students struggled")
        y -= 18
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
