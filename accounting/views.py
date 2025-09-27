from rest_framework import generics, permissions
from .models import Invoice
from rest_framework.serializers import ModelSerializer
class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
class InvoiceList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
