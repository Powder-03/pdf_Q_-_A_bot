from django.contrib import admin
from .models import Document, DocumentChunk

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_type', 'processed', 'upload_date']
    list_filter = ['file_type', 'processed', 'upload_date']
    search_fields = ['title']
    readonly_fields = ['id', 'upload_date']

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['document', 'chunk_index']
    list_filter = ['document']
    search_fields = ['content']