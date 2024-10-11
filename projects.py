# import PyPDF2
# import openai
# import re

# api_key = 

# def extract_text_from_pdf(path):
#     with open(path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ''
#         for page_num in range(len(reader.pages)):
#             page = reader.pages[page_num]
#             text += page.extract_text()
#         return text

# def extract_project_section(text):
#     match = re.search(r'\b(Projects|PROJECTS)\b', text, re.IGNORECASE)

#     if not match:
#         return None  # Return None if "EXPERIENCE" section is not found
    
#     start = match.start()
#     experience_section = text[start:]

#     # Stop extraction at the next major section like "PROJECTS", "TECHNICAL SKILLS", etc.
#     section_end = re.search(r'\b(CERTIFICATES|TECHNICAL SKILLS|ACHIEVEMENTS|EDUCATION)\b', experience_section,  re.IGNORECASE)
#     if section_end:
#         experience_section = experience_section[:section_end.start()]

#     return experience_section.strip()


# def extract_project_skills(experience_text):
#     if experience_text is None:
#         return None  # Handle the case where experience text is None

#     openai.api_key = api_key  # Replace with your OpenAI API key

#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": (
#                 f'''Extract the output in the specified JSON format for each individual experience of the candidate, including the following fields:

                    
#                     Project Name
#                     Framework: A tool in programming that provides ready-made components or solutions customized for speed development.
#                     Programming Language: A computer language used by developers to communicate with computers, consisting of instructions written in a specific language to perform tasks.
#                     Tools: Computer programs that assist software developers in creating applications.
#                     Database
#                     Cloud

#                 {experience_text}
#                 '''
#             )
#         }
#     ]

#     response = openai.chat.completions.create(
#         model="gpt-4o-mini",  # Use a more specific model if available
#         messages=messages
#     )

#     return response.choices[0].message.content  # Correct way to access content

# def process_resume(path):
#     extracted_text = extract_text_from_pdf(path)
    
#     project_section = extract_project_section(extracted_text)
#     # print("Extracted Experience Section:")
#     # print(project_section)

    

#     skills_json = extract_project_skills(project_section)
    

#     return skills_json

# pdf_file_path = r"C:\Users\Dhruv Adavadkar\OneDrive\Desktop\Dhruv_adavadkar_resume.pdf"
# skills = process_resume(pdf_file_path)
# print("Project Skills JSON:", skills)

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

# Function to extract the project section from the resume text
def extract_project_section(text):
    match = re.search(r'\b(Projects|PROJECTS|PROJECT Work|PROJECT DETAILS)\b', text, re.IGNORECASE)
    
    if not match:
        return None  # Return None if the "Projects" section is not found
    
    start = match.start()
    project_section = text[start:]
    
    # Stop extraction at the next major section
    section_end = re.search(r'\b(CERTIFICATES|CERTIFICATIONS|TECHNICAL SKILLS|ACHIEVEMENTS|EDUCATION)\b', project_section, re.IGNORECASE)
    if section_end:
        project_section = project_section[:section_end.start()]
    
    return project_section.strip()

# Function to extract skills from the project section using the LLM
def extract_project_skills(project_text):
    if not project_text:
        return "No project section found in the resume."
    
    try:
        # Define the prompt using Langchain's prompt template
        prompt = ChatPromptTemplate.from_template(
            '''
            Extract the following information from the project section in JSON format:
            - Project Name
            - Framework: A framework in programming is a tool that provides ready-made components or solutions that are customized for speed development.
            - Programming Language: It is a computer lang that is used by the developers to communicate with computers. It is a set of instructions written in any specific lang to perform a task.
            - Tools: tool refers to any software or utility that helps developers create, test, debug, or maintain their code more efficiently. These tools automate or simplify various aspects of the software development process, improving productivity and ensuring higher code quality.
            - Database
            - cloud Technology : Cloud technology refers to the delivery of computing services—including storage, processing power, databases, networking, software, and analytics—over the internet
            - Time : Give then time frame the candidate was in that company in months
            
            Here is the project section:
            {project_text}
            '''
        )

        # Format the prompt with the provided project text
        formatted_prompt = prompt.format(project_text=project_text)

        # Call the LLM using the new method (invoke)
        response = llm.invoke(formatted_prompt)  # Use 'invoke' instead of __call__

        # Get the content from the response (AIMessage)
        return response.content  # Extract the actual message content

    except Exception as e:
        return f"Error during LLM call: {e}"

# Function to process the resume and extract project skills
def process_resume(path):
    extracted_text = extract_text_from_pdf(path)
    
    if not extracted_text:
        return "Failed to extract text from the PDF."

    # Extract the project section from the resume
    project_section = extract_project_section(extracted_text)
    # print("Extracted Project Section:\n", project_section)

    # Extract the skills as JSON using the LLM
    skills_json = extract_project_skills(project_section)

    return skills_json

# Path to the resume PDF file
pdf_file_path = r"C:\Users\Dhruv Adavadkar\Downloads\Datacom\Datacom\KumarGaurav[3_10] (1).pdf"


# Run the process_resume function
skills = process_resume(pdf_file_path)

# Output the result
print("Project Skills JSON:", skills)



