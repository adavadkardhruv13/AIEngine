# import PyPDF2
# import re
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI  # Updated import
# from langchain.prompts import ChatPromptTemplate


# # Load environment variables from .env file
# load_dotenv()

# # Get the OpenAI API key from environment variables
# openai_api_key = os.getenv("OPENAI_API_KEY")
# if not openai_api_key:
#     raise ValueError("OpenAI API key not found. Please set it in your .env file.")

# # Initialize the LLM model using Langchain
# llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=openai_api_key)

# # Function to extract text from a PDF
# def extract_text_from_pdf(path):
#     try:
#         with open(path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ''
#             for page_num in range(len(reader.pages)):
#                 page = reader.pages[page_num]
#                 text += page.extract_text() or ""  # Safeguard against None
#             return text.strip() if text.strip() else None  # Return None if text is empty
#     except Exception as e:
#         print(f"Error reading PDF: {e}")
#         return None

# # Function to extract the experience section from the resume text
# def extract_experience_section(text):
#     match = re.search(r'\b(EXPERIENCE|Work Experience|Work experience|WORK PROFICIENCY|PROFESSIONAL EXPERIENCE)\b', text, re.IGNORECASE)
    
#     if not match:
#         return None  # Return None if the "experience" section is not found
    
#     start = match.start()
#     experience_section = text[start:]
    
#     # Stop extraction at the next major section
#     section_end = re.search(r'\b(PROJECTS|CERTIFICATES|CERTIFICATIONS|TECHNICAL SKILLS|ACHIEVEMENTS|EDUCATION)\b', experience_section, re.IGNORECASE)
#     if section_end:
#         experience_section = experience_section[:section_end.start()]
    
#     return experience_section.strip()

# # Function to extract skills from the experience section using the LLM
# def extract_experience_skills(experience_text):
#     if not experience_text:
#         return "No experience section found in the resume."
    
#     try:
#         # Define the prompt using Langchain's prompt template
#         prompt = ChatPromptTemplate.from_template(
#             '''
#             Extract the following information from the experience section in JSON format with consistent structure, regardless of the content. Ensure the following keys are always present:

#             - "total_years_of_experience": Overall experience that a candidate is having in their career
#             - "projects": A list of projects. Each project should have:
#                 - "project_name": Name of the project
#                 - "framework": The framework(s) used (e.g., React, Django). Default to "N/A" if not applicable.
#                 - "programming_language": The programming language(s) used (e.g., Python, C++). Default to "N/A" if not applicable.
#                 - "tools": The tools used (e.g., Git, Docker). Default to "N/A" if not applicable.
#                 - "database": The database used, if any. Default to "N/A" if not applicable.
#                 - "cloud_technology": Cloud technology used, if any. Default to "N/A" if not applicable.
#                 - "time": Time spent on the project in months as a numeric value (e.g., 6 for 6 months, 12 for 12 months). Default to 0 if not mentioned.

#             Ensure the JSON structure is maintained even if some fields are missing, and ensure that 'time' is represented by a numeric value only.

#             Here is the experience section:
#             {experience_text}
#             '''
#         )

#         # Format the prompt with the provided experience text
#         formatted_prompt = prompt.format(experience_text=experience_text)

#         # Call the LLM using the new method (invoke)
#         response = llm.invoke(formatted_prompt)  # Use 'invoke' instead of __call__

#         # Get the content from the response (AIMessage)
#         return response.content  # Extract the actual message content

#     except Exception as e:
#         return f"Error during LLM call: {e}"

# # Function to process the resume and extract experience skills
# def process_experience(path):
#     extracted_text = extract_text_from_pdf(path)
    
#     if not extracted_text:
#         return "Failed to extract text from the PDF."

#     # Extract the experience section from the resume
#     experience_section = extract_experience_section(extracted_text)
#     # print("Extracted experience Section:\n", experience_section)

#     # Extract the skills as JSON using the LLM
#     skills_json = extract_experience_skills(experience_section)

#     return skills_json

# # Path to the resume PDF file
# pdf_file_path = r"C:\Users\Dhruv Adavadkar\Downloads\Datacom\Datacom\manishkumar[5_6] (1) (1).pdf"
# # Run the process_resume function
# skills = process_experience(pdf_file_path)

# # Output the result 
# print("Experience Skills JSON:", skills)  



# from langchain.prompts import PromptTemplate
# from langchain_openai  import OpenAI
# from langchain.chains import LLMChain
# from langchain_core import RunnableSequence
# import PyPDF2
# import json

# def extract_text_from_pdf(path):
#     with open(path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ''
#         for page_num in range(len(reader.pages)):
#             page = reader.pages[page_num]
#             text += page.extract_text()
#         return text

# # Define the prompt template
# prompt_template = """
# You are given the following text from a resume:

# {resume_text}

# Please extract the key skills from the following experience section in the JSON format:

# Example JSON format:

# {{
#     'framework': {{ 'React': '<time>', 'Django': '<time>' }},
#     'prog_lang': {{ 'JavaScript': '<time>', 'Python': '<time>' }},
#     'role': {{ 'developer': '<time>' }},
#     'domain': {{ }},
#     'tools': {{ 'Ansible': '<time>' }},
#     'time': 'time period of project in months'
# }}
# """

# # Define the PromptTemplate
# prompt = PromptTemplate(
#     input_variables=['resume_text'],
#     template=prompt_template
# )

# # Instantiate the LLM from langchain_community
# llm = OpenAI(temperature=0, openai_api_key="

# # Create an LLMChain
# chain =  RunnableSequence(prompt=prompt, llm=llm)

# def process_resume(path):
#     resume_text = extract_text_from_pdf(path)

#     # Run the chain using invoke
#     response = chain.run({'resume_text': resume_text})

#     try:
#         # Try to parse the response into JSON format
#         json_response = json.loads(response)
#     except json.JSONDecodeError:
#         print("Failed to parse JSON. Here's the raw response:")
#         print(response)
#         json_response = None

#     return json_response

# # Example path for the PDF
# path = r"C:\Users\Dhruv Adavadkar\OneDrive\Desktop\Dhruv_adavadkar_resume.pdf"

# experience_section = process_resume(path)

# # Pretty print the JSON output if available
# if experience_section:
#     print(json.dumps(experience_section, indent=4))




import PyPDF2
import re
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
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
def extract_text_from_pdf(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""  # Safeguard against None
            return text.strip() if text.strip() else None  # Return None if text is empty
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Function to extract the experience section from the resume text
def extract_experience_section(text):
    match = re.search(r'\b(EXPERIENCE|Work Experience|Work experience|WORK PROFICIENCY|PROFESSIONAL EXPERIENCE|Professional Experience)\b', text, re.IGNORECASE)
    
    if not match:
        return None  # Return None if the "experience" section is not found
    
    start = match.start()
    experience_section = text[start:]
    
    # Stop extraction at the next major section
    section_end = re.search(r'\b(CERTIFICATES|CERTIFICATIONS|TECHNICAL SKILLS|ACHIEVEMENTS|EDUCATION)\b', experience_section, re.IGNORECASE)
    if section_end:
        experience_section = experience_section[:section_end.start()]
    
    return experience_section.strip()

# Function to extract skills from the experience section using the LLM
def extract_experience_skills(experience_text):
    if not experience_text:
        return "No experience section found in the resume."
    
    try:
        # Define the prompt using Langchain's prompt template
        prompt = ChatPromptTemplate.from_template(
            '''
            Extract the following information from the experience section in JSON format with consistent structure, regardless of the content. Ensure the following keys are always present:

            - "total_years_of_experience": Overall experience that a candidate is having in his career
            - "projects": A list of projects. Each project should have:
                - "project_name": Name of the project
                - "framework": The framework(s) used (e.g., React, Django). Default to "N/A" if not applicable.
                - "programming_language": The programming language(s) used (e.g., Python, C++). Default to "N/A" if not applicable.
                - "tools": The tools used (e.g., Git, Docker). Default to "N/A" if not applicable.
                - "database": The database used, if any. Default to "N/A" if not applicable.
                - "cloud_technology": Cloud technology used, if any. Default to "N/A" if not applicable.
                - "time": Time spent on the project in months.(only numbers in months)

            Ensure the JSON structure is maintained even if some fields are missing.

            Here is the experience section:
            {experience_text}
            '''
        )

        # Format the prompt with the provided experience text
        formatted_prompt = prompt.format(experience_text=experience_text)

        # Call the LLM using the new method (invoke)
        response = llm.invoke(formatted_prompt)  # Use 'invoke' instead of __call__

        # Get the content from the response (AIMessage)
        return response.content  # Extract the actual message content

    except Exception as e:
        return f"Error during LLM call: {e}"

# Function to process the resume and extract experience skills
def process_experience(pdf_file_path):
    extracted_text = extract_text_from_pdf(pdf_file_path)
    
    if not extracted_text:
        return "Failed to extract text from the PDF."

    # Extract the experience section from the resume
    experience_section = extract_experience_section(extracted_text)

    # Extract the skills as JSON using the LLM
    skills_json = extract_experience_skills(experience_section)

    return skills_json

# Path to the resume PDF file
pdf_file_path = r"C:\Users\Dhruv Adavadkar\Downloads\Datacom\Datacom\Nitesh_Kumar_2_Year(s)_1_Month(s)_Noida_15_Dec_1993 (1).pdf"
skills = process_experience(pdf_file_path)

# Output the result 
print("Experience Skills JSON:", skills)