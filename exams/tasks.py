from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Result
from reports.student_pdf import generate_student_report
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_guardian_result_email(self, result_id):
    try:
        r = Result.objects.select_related('student__user','exam','student__guardian').get(id=result_id)
        guardian = r.student.guardian
        if not guardian or not guardian.email:
            return 'no-guardian'
        context = {
            'guardian_name': guardian.get_full_name() or guardian.username,
            'student_name': r.student.user.get_full_name(),
            'exam_title': r.exam.title,
            'percent': round(r.percent, 1),
            'breakdown': r.breakdown,
            'career_advice': r.career_advice,
        }
        subject = f"Exam Results for {context['student_name']} — {r.exam.title}"
        html_body = render_to_string('emails/guardian_result.html', context)
        text_body = f"{context['student_name']} scored {context['percent']}% in {r.exam.title}."
        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [guardian.email])
        msg.attach_alternative(html_body, 'text/html')
        try:
            pdf_buffer = generate_student_report(r.student, {
                'exam': r.exam.title,
                'total_score': r.total_score,
                'percentage': r.percent,
                'breakdown': {k: v['percent'] for k, v in r.breakdown.get('topic_scores', {}).items()},
                'weak_topics': r.breakdown.get('weak_topics', []),
                'career_advice': r.career_advice
            })
            msg.attach(f"{r.student.user.username}_{r.exam.id}.pdf", pdf_buffer.getvalue(), 'application/pdf')
        except Exception:
            pass
        msg.send()
        return 'sent'
    except Result.DoesNotExist:
        return 'missing'
    except Exception as e:
        raise self.retry(exc=e)
