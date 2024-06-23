
from django.db import models
from django.contrib.auth.models import User

class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExtractedContent(models.Model):
    pdf_document = models.OneToOneField(PDFDocument, on_delete=models.CASCADE)
    content = models.TextField()
    extracted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Extracted content for {self.pdf_document.title}"