from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer, QuestionSerializer
from .services import DocumentProcessor
import os

class DocumentListView(generics.ListAPIView):
    """GET API: Retrieve all uploaded documents"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    """POST API: Upload and process documents"""

    @swagger_auto_schema(
        operation_description="Upload and process a document (PDF/DOCX/TXT)",
        responses={201: openapi.Response("Document uploaded", DocumentSerializer)},
        consumes=["multipart/form-data"]
    )
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Get file extension
            file = serializer.validated_data['file']
            file_extension = file.name.split('.')[-1].lower()
            
            # Create document instance
            document = serializer.save(file_type=file_extension)
            
            # Process document in background (you might want to use Celery for this)
            processor = DocumentProcessor()
            success = processor.process_document(document)
            
            if success:
                return Response({
                    'message': 'Document uploaded and processed successfully',
                    'document': DocumentSerializer(document).data
                }, status=status.HTTP_201_CREATED)
            else:
                # Delete document if processing failed
                document.delete()
                return Response({
                    'error': 'Failed to process document'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentQuestionView(APIView):
    """POST API: Ask questions about documents (RAG query endpoint)"""

    @swagger_auto_schema(
        operation_description="Ask a question about a document (RAG query endpoint)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'document_id': openapi.Schema(type=openapi.TYPE_STRING, description='Document UUID'),
                'question': openapi.Schema(type=openapi.TYPE_STRING, description='Question to ask about the document'),
                'search_kwargs': openapi.Schema(type=openapi.TYPE_OBJECT, description='Optional search kwargs', default={}),
            },
            required=['document_id', 'question'],
        ),
        responses={200: openapi.Response("Answer returned")},
        consumes=["application/json"]
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            document_id = serializer.validated_data['document_id']
            question = serializer.validated_data['question']
            search_kwargs = serializer.validated_data.get('search_kwargs', {})
            
            # Check if document exists and is processed
            document = get_object_or_404(Document, id=document_id)
            if not document.processed:
                return Response({
                    'error': 'Document is not yet processed. Please wait and try again.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Process question
            processor = DocumentProcessor()
            answer = processor.ask_question(document_id, question, search_kwargs)
            
            return Response({
                'question': question,
                'answer': answer,
                'document_id': str(document_id),
                'search_kwargs': search_kwargs
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
