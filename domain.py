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

def candidate_domain(skills_json):
    try:
        # Define the prompt for domain inference
        prompt = ChatPromptTemplate.from_template(
            '''
                Based on the following extracted skills and experience details from a candidate's resume, identify the most relevant domain or field of expertise. Consider the frameworks, programming languages, tools, databases, cloud technologies, and job roles mentioned. Provide a concise answer representing the candidate's primary domain of expertise (e.g., "Web Development", "Data Science", "Cloud Engineering", "Cybersecurity", "DevOps", etc.).
                give in single word.
            Skills JSON:
            {skills_json}
            
            '''
        )

        # Format the prompt with the extracted skills JSON
        formatted_prompt = prompt.format(skills_json=skills_json)

        # Call the LLM to infer the domain
        response = llm.invoke(formatted_prompt)

        # Return the inferred domain
        return response.content  # Extract the message content (domain)

    except Exception as e:
        return f"Error during domain inference: {e}"

# Function to process the resume and extract both skills and domain
def process_resume(path):
    extracted_text = extract_text_from_pdf(path)
    
    if not extracted_text:
        return "Failed to extract text from the PDF."

    # Extract the skills as JSON using the LLM
    skills_json = extract_experience_skills(extracted_text)
    # print("Extracted Skills JSON:\n", skills_json)

    # Use the extracted skills to infer the candidate's domain
    domain = candidate_domain(skills_json)
    print("Candidate Domain:\n", domain)

    # return {
    #     "skills": skills_json,
    #     "domain": candidate_domain
    # }

# Path to the resume PDF file
pdf_file_path = r"C:\Users\Dhruv Adavadkar\Downloads\Datacom\Datacom\Nitesh_Kumar_2_Year(s)_1_Month(s)_Noida_15_Dec_1993 (1).pdf"
# Run the process_resume function
result = process_resume(pdf_file_path)
