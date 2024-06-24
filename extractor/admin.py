from django.contrib import admin
from .models import PDFDocument, ExtractedContent

# Register your models here.


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    list_filter = ('user', 'uploaded_at')
    search_fields = ('title', 'user__username')

@admin.register(ExtractedContent)
class ExtractedContentAdmin(admin.ModelAdmin):
    list_display = ('pdf_document', 'extracted_at')
    list_filter = ('extracted_at',)
    search_fields = ('pdf_document__title',)
