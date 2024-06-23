from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from .openai_utils import extract_data_from_pdf

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_path = default_storage.save(f'temp/{file.name}', file)
        extracted_data = extract_data_from_pdf(file_path)
        os.remove(file_path) 
        return JsonResponse(extracted_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
