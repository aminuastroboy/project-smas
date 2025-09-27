from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Exam, Result
from .serializers import ResultSerializer, ExamSerializer
from .utils import compute_breakdown
from users.models import Student
from django.utils import timezone
from .tasks import send_guardian_result_email
class SubmitExamView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return Response({'detail': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail': 'Student profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        answers = request.data.get('answers', {})
        breakdown = compute_breakdown(exam, answers)
        total_score = sum(item['score'] for item in breakdown['question_scores'])
        percent = (total_score / exam.total_marks) * 100 if exam.total_marks else 0
        career_advice = []
        topic_scores = breakdown.get('topic_scores', {})
        if topic_scores.get('Mathematics', {}).get('percent', 0) >= 75:
            career_advice.append('Strong in Mathematics — consider Engineering or Data Science')
        result = Result.objects.create(
            exam=exam, student=student, total_score=total_score,
            percent=percent, breakdown=breakdown, career_advice=career_advice,
            graded=True, graded_at=timezone.now()
        )
        send_guardian_result_email.delay(result.id)
        return Response(ResultSerializer(result).data, status=status.HTTP_201_CREATED)
class GetMyResultsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'detail':'Student profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        results = Result.objects.filter(student=student)
        return Response(ResultSerializer(results, many=True).data)
