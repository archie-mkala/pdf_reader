from django.urls import path
from .views import PDFUploadView, PDFDetailView, PDFListView, index

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),  
    path('upload/', PDFUploadView.as_view(), name='upload_pdf'), 
    path('pdfs/', PDFListView.as_view(), name='pdf-list'),
    path('pdfs/<int:pk>/', PDFDetailView.as_view(), name='pdf-detail'),
]
