import os
from flask import Flask, request, jsonify, make_response
import json
import re
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import google.generativeai as genai
from models import Question, db
import requests
import PyPDF2  # Library to extract text from PDF

# Load environment variables from .env file
load_dotenv()

# Configure SQLite database
DATABASE_URL = 'sqlite:///scores.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
db.metadata.create_all(engine)

# Configure the Gemini API with the retrieved API key
genai.configure(api_key="AIzaSyC42bClVHR9354UFmUS8OxxociLU23T5Ns")

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

# Template for generating QCM based on a job description
template = """
You are an AI front-end developer and an assistant that generates QCM questions strictly to evaluate a candidate's skills and knowledge based on the "Compétences Techniques" and "Responsabilité" sections of the following job description. Please generate 10 advanced 1 answer questions, including the correct answers, formatted as JSON.

The JSON structure should include:
- A list of questions.
- Each question should have:
  - "question": The text of the question.
  - "options": A list of multiple-choice options.
  - "answer": The correct answer.

Strict Guidelines:
- **Only generate questions that test the candidate's understanding and skills**, based on the technologies and responsibilities mentioned in the "Compétences Techniques" and "Responsabilité" sections.
- **Do not ask candidates to recall details directly from the job description.** Instead, ask questions that assess their knowledge of how to apply these skills and handle these responsibilities in real-world scenarios.
- **Questions should be practical and skill-based,** aimed at testing the candidate's competency in the relevant technical areas and responsibilities.
- Avoid speculative or hypothetical questions.

Job Description:
{job_description}

Generate the JSON:
"""



# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
# Function to fetch the PDF from the offer-service
def fetch_pdf_from_offer_service(offer_id):
    url = f'http://offer-service:8040/api/v1/offers/file/{offer_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the PDF locally
            pdf_path = f"offer_{offer_id}.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            return pdf_path
        else:
            print(f"Failed to fetch PDF, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching PDF from offer-service: {e}")
        return None

# Function to generate QCM questions based on the job description
def generate_q(job_description):
    prompt = template.format(job_description=job_description)
    response = model.generate_content(prompt)

    # Log the raw response for debugging
    print(f"Raw API response: {response}")

    if response and response.parts:
        generated_json = "".join([part.text for part in response.parts])

        # Remove the markdown block markers (```json and ```).
        cleaned_json = re.sub(r'```json|```', '', generated_json)
        print(f"Cleaned JSON: {cleaned_json}")  # Log the cleaned JSON

        return cleaned_json
    else:
        print("No response or empty parts from the model")
        return ""

# Function to process the job description and save questions with test_id
def process_job_description(offer_id, test_id):
    # Fetch the PDF from offer-service
    pdf_path = fetch_pdf_from_offer_service(offer_id)
    if not pdf_path:
        return "Unable to fetch the PDF from offer-service."

    # Extract job description from the PDF file
    job_description = extract_text_from_pdf(pdf_path)
    
    # Check if the job description is provided
    if not job_description:
        return "No job description provided or unable to extract text from the PDF."

    generated_json = generate_q(job_description)

    # Check if the JSON is empty
    if not generated_json:
        return "No questions generated. Please check the job description or API response."

    try:
        # Parse the generated JSON
        questions = json.loads(generated_json)
        print(f"Parsed Questions: {questions}")  # Log the parsed questions
    except json.JSONDecodeError as e:
        # Return an error if JSON is invalid
        return f"Error decoding JSON: {e}"

    # Save each question in the database with test_id
    try:
        for q in questions:
            new_question = Question(
                test_id=test_id,  # Use test_id to link the question with the test
                question_text=q['question'],
                options=json.dumps(q['options']),  # Store as a JSON string
                correct_answer=q['answer']
            )
            session.add(new_question)

        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

    return f"{generated_json}"

# Flask app to accept REST requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    offer_id = data.get('offer_id')
    test_id = data.get('test_id')

    if not offer_id or not test_id:
        return jsonify({"error": "offer_id and test_id are required"}), 400

    result = process_job_description(offer_id, test_id)

    # Create a response object
    response = make_response(result)
    
    # Set the content type to JSON
    response.headers['Content-Type'] = 'application/json'
    
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)