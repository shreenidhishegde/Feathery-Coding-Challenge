# Document Extractor

Document Extractor is a Django-based web application that allows users to upload PDF documents, extract content from them, and view the extracted content.
It uses OpenAI’s vision model to extract a few pieces of structured information from the
file.

## Features

- User authentication (login, registration)
- Upload PDF documents
- Extract content from uploaded PDFs:
    i. Account owner name
    ii. Portfolio value
    iii. Name and cost basis of each holding
- View extracted content
- Pagination for viewing multiple PDFs

## Requirements

- Python 3.x
- Django 4.x
- Django REST framework
- Pillow

## Installation

1. **Clone the repository:**

   ```bash
   `git clone https://github.com/yourusername/document_extractor.git`
   `cd document_extractor`
   RUN `python manage.py runserver`