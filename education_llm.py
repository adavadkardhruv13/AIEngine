import PyPDF2
import re
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Updated import
from langchain.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in your .env file.")

# Initialize the LLM model using Langchain
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=openai_api_key)

# Function to extract text from a PDF
def extract_text_from_pdf(path):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""  # Safeguard against None
            return text.strip() if text.strip() else None  # Return None if text is empty
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Function to extract the education section from the resume text
def extract_education_section(text):
    match = re.search(r'\b(EDUCATION|Education Qualification|Academic Background|QUALIFICATION|Professional Education)\b', text, re.IGNORECASE)
    
    if not match:
        return None  # Return None if the "education" section is not found
    
    start = match.start()
    education_section = text[start:]
    
    # Stop extraction at the next major section
    section_end = re.search(r'\b(EXPERIENCE|PROJECTS|TECHNICAL SKILLS|ACHIEVEMENTS|PERSONAL TRAITS|CERTIFICATES)\b', education_section, re.IGNORECASE)
    if section_end:
        education_section = education_section[:section_end.start()]
    
    return education_section.strip()

# Function to extract skills from the education section using the LLM
def extract_education_skills(education_text):
    if not education_text:
        return "No education section found in the resume."
    
    try:
        # Define the prompt using Langchain's prompt template
        prompt = ChatPromptTemplate.from_template(
            '''
            Parse the given education text to extract only one latest educational information and return a JSON object containing 
                the following fields:

                        - Institution
                        - Degree
                        - CGPA
                        - Year of course end

                {education_text}
                '''
        )

        # Format the prompt with the provided education text
        formatted_prompt = prompt.format(education_text=education_text)

        # Call the LLM using the new method (invoke)
        response = llm.invoke(formatted_prompt)  # Use 'invoke' instead of __call__

        # Get the content from the response (AIMessage)
        return response.content  # Extract the actual message content

    except Exception as e:
        return f"Error during LLM call: {e}"

# Function to process the resume and extract education skills
def process_education(path):
    extracted_text = extract_text_from_pdf(path)
    
    if not extracted_text:
        return "Failed to extract text from the PDF."

    # Extract the education section from the resume
    education_section = extract_education_section(extracted_text)
    # print("Extracted education Section:\n", education_section)

    # Extract the skills as JSON using the LLM
    skills_json = extract_education_skills(education_section)

    return skills_json

# Path to the resume PDF file
pdf_file_path = r"C:\Users\Dhruv Adavadkar\Downloads\Datacom\Datacom\Nitesh_Kumar_2_Year(s)_1_Month(s)_Noida_15_Dec_1993 (1).pdf"

# Run the process_resume function
skills = process_education(pdf_file_path)

# Output the result
print("education Skills JSON:", skills)