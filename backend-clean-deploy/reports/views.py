from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .tasks import send_reports_for_class
from celery.result import AsyncResult

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_reports(request, class_id):
    teacher_email = request.user.email
    task = send_reports_for_class.delay(class_id, teacher_email)
    return Response({'task_id': task.id, 'status': 'Started'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_status(request, task_id):
    result = AsyncResult(task_id)
    return Response({'task_id': task_id, 'state': result.state, 'info': result.info if result.info else {}})
