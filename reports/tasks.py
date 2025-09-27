from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from reports.class_pdf import generate_class_report
from exams.models import Result
from users.models import Student, ClassRoom
@shared_task(bind=True)
def send_reports_for_class(self, class_id, teacher_email):
    classroom = ClassRoom.objects.get(id=class_id)
    students = Student.objects.filter(classroom=classroom)
    total = students.count()
    for i, student in enumerate(students, start=1):
        latest = Result.objects.filter(student=student).order_by('-created_at').first()
        if not latest:
            self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'student': student.user.username})
            continue
        result_data = {
            'exam': latest.exam.title,
            'total_score': latest.total_score,
            'percentage': latest.percent,
            'breakdown': {k: v['percent'] for k, v in latest.breakdown.get('topic_scores', {}).items()},
            'weak_topics': latest.breakdown.get('weak_topics', []),
            'career_advice': latest.career_advice
        }
        guardian_email = student.guardian.email if student.guardian else None
        if guardian_email:
            try:
                from reports.student_pdf import generate_student_report
                pdf_buffer = generate_student_report(student, result_data)
                msg = EmailMessage(f"{student.user.get_full_name()} - Exam Report", f"Attached is the report for {student.user.get_full_name()}", settings.DEFAULT_FROM_EMAIL, [guardian_email])
                msg.attach(f"{student.user.username}_report.pdf", pdf_buffer.getvalue(), 'application/pdf')
                msg.send()
            except Exception:
                pass
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'student': student.user.username})
    analytics_data = {'average_scores': [], 'weak_topics': {}}
    try:
        pdf_buf = generate_class_report(analytics_data, class_name=classroom.name)
        msg = EmailMessage(f"{classroom.name} - Class Report", "Class performance report attached", settings.DEFAULT_FROM_EMAIL, [teacher_email])
        msg.attach(f"{classroom.name}_class_report.pdf", pdf_buf.getvalue(), 'application/pdf')
        msg.send()
    except Exception:
        pass
    return {'current': total, 'total': total, 'status': 'Completed'}
