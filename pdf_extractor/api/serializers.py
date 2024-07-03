from rest_framework import serializers
from .models import Pdf

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        fields = '__all__'
