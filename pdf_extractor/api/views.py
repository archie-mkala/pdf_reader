from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Pdf
from .serializers import PDFSerializer
from PyPDF2 import PdfReader
import spacy

nlp = spacy.load('en_core_web_sm')

class PDFUploadView(APIView):
    def post(self, request):
        pdf_file = request.FILES['pdf_file']
        email = request.data['email']
        
        if Pdf.objects.filter(email=email).exists():
            return Response({'error': 'A PDF with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        pdf = Pdf(email=email, pdf_file=pdf_file)
        pdf.save()
        
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        doc = nlp(text)
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        verbs = [token.text for token in doc if token.pos_ == "VERB"]
        
        pdf.content = text
        pdf.nouns = ", ".join(nouns)
        pdf.verbs = ", ".join(verbs)
        pdf.save()
        
        return Response({'message': 'PDF uploaded successfully'}, status=status.HTTP_201_CREATED)

class PDFDetailView(APIView):
    def get(self, request, pk):
        pdf = Pdf.objects.get(pk=pk)
        serializer = PDFSerializer(pdf)
        return Response(serializer.data)

class PDFListView(APIView):
    def get(self, request):
        pdfs = Pdf.objects.all()
        serializer = PDFSerializer(pdfs, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'index.html')
