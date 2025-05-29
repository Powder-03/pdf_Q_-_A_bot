from django.urls import path
from .views import DocumentListView, DocumentUploadView, DocumentQuestionView

urlpatterns = [
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/question/', DocumentQuestionView.as_view(), name='document-question'),
]