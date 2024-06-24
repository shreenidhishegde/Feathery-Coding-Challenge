from openai import OpenAI
import fitz  
from pdf2image import convert_from_path
from io import BytesIO
import base64
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def extract_images_from_pdf(file_path):
    images = convert_from_path(file_path)
    return images

def extract_data_from_pdf(file_path):
    # Extract text from PDF
    text = extract_text_from_pdf(file_path)
    # images = extract_images_from_pdf(file_path)
    # image_data = [convert_image_to_base64(image) for image in images]

    prompt = (
        "Extract the account owner name, portfolio value, and each holding's name "
        "and cost basis from this investment statement.\n\n"
        "Return the output in JSON format.\n\n"
        "Text from the document:\n" + text + "\n\n"
    )

    # Add image descriptions to the prompt
    # for i, img_str in enumerate(image_data):
    #     prompt += f"Image {i+1}: (base64 encoded)\n{img_str}\n\n"

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        return {'error': f"Failed to get completion from language model: {str(e)}"}

    # Parse response 
    response_text = completion.choices[0].message.content.strip()

    extracted_data = {
        'response': response_text  
    }
    
    return extracted_data
