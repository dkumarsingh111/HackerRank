from flask import Flask, render_template, request, redirect, url_for, flash
from pdfminer.high_level import extract_text
from docx import Document
from PIL import Image
import pytesseract
import os
import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store uploaded files
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create the folder if it doesn't exist

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

# Function to extract text from Word files
def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error extracting text from DOCX: {str(e)}"

# Function to extract text from images
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

# Function to perform Named Entity Recognition
def analyze_text(text):
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        return f"Error analyzing text: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    entities = []
    
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            # Ensure a valid file is uploaded
            if uploaded_file.filename == '':
                flash('No file selected. Please upload a file.', 'error')
                return redirect(request.url)

            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            # Extract text based on file type
            if uploaded_file.filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            elif uploaded_file.filename.endswith('.docx'):
                extracted_text = extract_text_from_docx(file_path)
            elif uploaded_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = extract_text_from_image(file_path)
            else:
                flash('Unsupported file format. Please upload a PDF, DOCX, or image file.', 'error')
                return redirect(request.url)

            # Perform analysis on the extracted text
            entities = analyze_text(extracted_text)

            # Optionally, remove the uploaded file after processing
            os.remove(file_path)

    return render_template('index.html', extracted_text=extracted_text, entities=entities)

if __name__ == '__main__':
    app.run(debug=True)
