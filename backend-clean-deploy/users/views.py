from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, StudentSerializer
from .models import Student

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class StudentList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

from exams.models import Result
from exams.serializers import ResultSerializer
class StudentResults(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        results = Result.objects.filter(student_id=pk).order_by('-created_at')
        return Response(ResultSerializer(results, many=True).data)
