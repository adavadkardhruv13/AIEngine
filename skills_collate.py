# skill_collate.py

# skills_collate.py
import json
from collections import defaultdict
from experience_llm import process_experience  # Assuming experience.py is in the same directory

# Final dictionary to hold collated data with times
final_json = {
    "JobRoles": [],  # Assuming JobRoles are to be added later
    "ProgrammingLanguages": defaultdict(int),
    "Tools": defaultdict(int),
    "CloudTechnologies": defaultdict(int),
    "TimeSpent": []
}

# Function to check if the value is valid (not "N/A" or empty)
def valid_value(value):
    return value and value != "N/A" and value != "Not specified"

# Path to the resume PDF file (adjust path as needed)
pdf_file_path = r"C:\Users\Dhruv Adavadkar\Downloads\Datacom\Datacom\Nitesh_Kumar_2_Year(s)_1_Month(s)_Noida_15_Dec_1993 (1).pdf"

# Get the JSON output from the experience section
skills_json = process_experience(pdf_file_path)

# Parse the JSON output from the experience processing
try:
    data = json.loads(skills_json)
except json.JSONDecodeError:
    print("Error: Unable to parse skills JSON from the LLM output.")
    data = None

if data:
    # Collating data and summing times for each skill
    for entry in data["projects"]:
        time_spent = entry.get("time", 0)

        # Currently, there are no job roles in your input data; you can modify it to include them if needed
        # Uncomment if job roles exist
        # if valid_value(entry.get("JobRole")):
        #     final_json["JobRoles"].append(entry["JobRole"])

        if valid_value(entry.get("programming_language")):
            # Split programming languages if multiple exist
            programming_languages = [lang.strip() for lang in entry["programming_language"].split(",")]
            for language in programming_languages:
                final_json["ProgrammingLanguages"][language] += time_spent

        if valid_value(entry.get("tools")):
            # Split tools if multiple exist
            tools = [tool.strip() for tool in entry["tools"].split(",")]
            for tool in tools:
                final_json["Tools"][tool] += time_spent

        if valid_value(entry.get("cloud_technology")):
            # Split cloud technologies if multiple exist
            cloud_techs = [cloud.strip() for cloud in entry["cloud_technology"].split(",")]
            for cloud in cloud_techs:
                final_json["CloudTechnologies"][cloud] += time_spent

        # Append the project name and time spent for output
        if valid_value(entry.get("project_name")):
            final_json["TimeSpent"].append(f"{entry['project_name']} for {entry['time']} months")

    # Convert defaultdict to dict for final output
    final_json["ProgrammingLanguages"] = dict(final_json["ProgrammingLanguages"])
    final_json["Tools"] = dict(final_json["Tools"])
    final_json["CloudTechnologies"] = dict(final_json["CloudTechnologies"])

    # Output the final JSON
    print(json.dumps(final_json, indent=4))
else:
    print("No valid data extracted from the resume.")






# import json
# from collections import defaultdict

# # Input JSON data
# data = {
#     "total_years_of_experience": 6,
#     "projects": [
#         {
#             "project_name": "SIP TERMINAL DEVELOPMENT",
#             "framework": "N/A",
#             "programming_language": "C/C++, XML",
#             "tools": "Source Insight, Beyond Compare, SVN, Linux, PUTTY, GDB, MS-Office",
#             "database": "N/A",
#             "cloud_technology": "N/A",
#             "time": 72
#         },
#         {
#             "project_name": "WebDSS",
#             "framework": "N/A",
#             "programming_language": "C/C++, HTML, WebSockets",
#             "tools": "Source Insight, Beyond Compare, SVN, Linux, PUTTY, GDB, MS-Office",
#             "database": "N/A",
#             "cloud_technology": "N/A",
#             "time": 1
#         }
#     ]
# }

# # Final dictionary to hold collated data with times
# final_json = {
#     "JobRoles": [],  # Assuming JobRoles are to be added later
#     "ProgrammingLanguages": defaultdict(int),
#     "Tools": defaultdict(int),
#     "CloudTechnologies": defaultdict(int),
#     "TimeSpent": []
# }

# # Function to check if the value is valid (not "N/A" or empty)
# def valid_value(value):
#     return value and value != "N/A" and value != "Not specified"

# # Collating data and summing times for each skill
# for entry in data["projects"]:
#     time_spent = entry.get("time", 0)

#     # Currently, there are no job roles in your input data; you can modify it to include them if needed
#     # Uncomment if job roles exist
#     # if valid_value(entry.get("JobRole")):
#     #     final_json["JobRoles"].append(entry["JobRole"])
    
#     if valid_value(entry.get("programming_language")):
#         # Split programming languages if multiple exist
#         programming_languages = [lang.strip() for lang in entry["programming_language"].split(",")]
#         for language in programming_languages:
#             final_json["ProgrammingLanguages"][language] += time_spent
    
#     if valid_value(entry.get("tools")):
#         # Split tools if multiple exist
#         tools = [tool.strip() for tool in entry["tools"].split(",")]
#         for tool in tools:
#             final_json["Tools"][tool] += time_spent
    
#     if valid_value(entry.get("cloud_technology")):
#         # Split cloud technologies if multiple exist
#         cloud_techs = [cloud.strip() for cloud in entry["cloud_technology"].split(",")]
#         for cloud in cloud_techs:
#             final_json["CloudTechnologies"][cloud] += time_spent
    
#     if valid_value(entry.get("time")):
#         # Here, we need to modify the message according to the input data structure
#         final_json["TimeSpent"].append(f"{entry['project_name']} for {entry['time']} months")

# # Convert defaultdict to dict for final output
# final_json["ProgrammingLanguages"] = dict(final_json["ProgrammingLanguages"])
# final_json["Tools"] = dict(final_json["Tools"])
# final_json["CloudTechnologies"] = dict(final_json["CloudTechnologies"])

# # Output the final JSON
# print(json.dumps(final_json, indent=4))
