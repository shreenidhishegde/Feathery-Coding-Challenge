from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import PDFDocument, ExtractedContent
from .forms import PDFUploadForm
from .openai_utils import extract_data_from_pdf
from django.contrib.auth import logout
from django.core.paginator import Paginator
import os
import json

@csrf_exempt
@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_doc = form.save(commit=False)
            pdf_doc.user = request.user
            pdf_doc.save()
            file_path = pdf_doc.file.path
            extracted_data = extract_data_from_pdf(file_path)
            try:
                response_data = json.loads(extracted_data['response'].strip('```json\n```'))
                ExtractedContent.objects.create(
                    pdf_document=pdf_doc,
                    content=json.dumps(response_data)
                )
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format', 'details': str(e)}, status=400)
            return redirect('pdf_list')
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = PDFUploadForm()
    return render(request, 'extractor/upload_pdf.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pdf_list')
    else:
        form = AuthenticationForm()
    return render(request, 'extractor/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'extractor/home.html')

@login_required
def pdf_list(request):
    pdfs = PDFDocument.objects.filter(user=request.user).order_by('-uploaded_at')
    paginator = Paginator(pdfs, 1)  # Show 1 PDF per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pdf_data = []
    for pdf in page_obj:
        try:
            extracted_content = ExtractedContent.objects.get(pdf_document=pdf)
            content = json.loads(extracted_content.content)
        except ExtractedContent.DoesNotExist:
            content = None
        except json.JSONDecodeError as e:
            content = {'error': 'Invalid JSON format', 'details': str(e)}
        pdf_data.append({'pdf': pdf, 'content': content})

    return render(request, 'extractor/pdf_list.html', {'pdf_data': pdf_data, 'page_obj': page_obj})


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pdf_list')
    else:
        form = UserCreationForm()
    return render(request, 'extractor/register.html', {'form': form})