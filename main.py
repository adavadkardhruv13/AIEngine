import json
import argparse
from education_llm import process_education
from experience_llm import process_experience

def combine_outputs(education_data, experience_data):
    return{
        "education": education_data,
        "experience": experience_data
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process resume for education and experience details.")
    parser.add_argument("pdf_file_path", help="Path to the resume PDF file.")
    parser.add_argument("--output", help="Path to save the combined result as JSON.", default=None)

    args = parser.parse_args()

    # Process both education and experience sections
    education_data = process_education(args.pdf_file_path)
    experience_data = process_experience(args.pdf_file_path)

    # Combine the results
    combined_data = combine_outputs(education_data, experience_data)

    # Print combined result
    print("Combined JSON Output:", json.dumps(combined_data, indent=4))

    # Optionally save to JSON file if output path is provided
    if args.output:
        with open(args.output, 'w') as json_file:
            json.dump(combined_data, json_file, indent=4)
        print(f"Combined data saved to {args.output}")