from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'file_type', 'upload_date', 'processed']
        read_only_fields = ['id', 'upload_date', 'processed', 'file_type']

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['title', 'file']
    
    def validate_file(self, value):
        allowed_extensions = ['pdf', 'txt', 'docx']
        extension = value.name.split('.')[-1].lower()
        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"File type '{extension}' not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        return value

class QuestionSerializer(serializers.Serializer):
    document_id = serializers.UUIDField()
    question = serializers.CharField(max_length=1000)
    search_kwargs = serializers.DictField(required=False, default=dict)
    
    def validate_search_kwargs(self, value):
        if 'k' in value:
            k = value['k']
            if not isinstance(k, int) or k < 3 or k > 5:
                raise serializers.ValidationError("'k' must be an integer between 3 and 5")
        return value