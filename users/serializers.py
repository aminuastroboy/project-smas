from rest_framework import serializers
from .models import User, Student
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','is_student','is_teacher','is_guardian']
class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = Student
        fields = ['id','name','classroom','guardian']
