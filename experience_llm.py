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

# Function to extract the experience section from the resume text
def extract_experience_section(text):
    match = re.search(r'\b(EXPERIENCE|Work Experience|Work experience|WORK PROFICIENCY|PROFESSIONAL EXPERIENCE)\b', text, re.IGNORECASE)
    
    if not match:
        return None  # Return None if the "experience" section is not found
    
    start = match.start()
    experience_section = text[start:]
    
    # Stop extraction at the next major section
    section_end = re.search(r'\b(PROJECTS|CERTIFICATES|CERTIFICATIONS|TECHNICAL SKILLS|ACHIEVEMENTS|EDUCATION)\b', experience_section, re.IGNORECASE)
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
            Extract the following information from the experience section in JSON format with different or sub json for different project in the company:
            - Total years of experience: Overall experience that a candidate is having in his career
            - Job Role: A position or job title assigned to an employee within an organization.
            - Company Name
            - Framework: A framework in programming is a tool that provides ready-made components or solutions that are customized for speed development and show with time.
            - Programming Language: It is a computer lang that is used by the developers to communicate with computers. It is a set of instructions written in any specific lang to perform a task and show with time.
            - Tools: tool refers to any software or utility that helps developers create, test, debug, or maintain their code more efficiently. These tools automate or simplify various aspects of the software development process, improving productivity and ensuring higher code quality and show with time.
            - Database
            - cloud Technology : Cloud technology refers to the delivery of computing services—including storage, processing power, databases, networking, software, and analytics—over the internet and show with time.
            - Time : Time that a candidate was in that perticular projects in months
            
            
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
def process_experience(path):
    extracted_text = extract_text_from_pdf(path)
    
    if not extracted_text:
        return "Failed to extract text from the PDF."

    # Extract the experience section from the resume
    experience_section = extract_experience_section(extracted_text)
    # print("Extracted experience Section:\n", experience_section)

    # Extract the skills as JSON using the LLM
    skills_json = extract_experience_skills(experience_section)

    return skills_json

# Path to the resume PDF file
pdf_file_path = r"C:\Users\Dhruv Adavadkar\OneDrive\Desktop\Dhruv_adavadkar_resume.pdf"
# Run the process_resume function
skills = process_experience(pdf_file_path)

# Output the result 
print("Experience Skills JSON:", skills)    
