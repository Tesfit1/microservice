import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import requests
import json

# Load environment variables from .env file

# Load environment variables from .env file
load_dotenv()
#1.Create Subjects
# variables 
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
SESSION_ID = os.getenv("SESSION_ID")
study_country = "Germany"  # Example country, change it as needed
study_name = 'HPC_Test_Study_DEV1'
site = 'DEU1'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    "Authorization": f"Bearer {SESSION_ID}",  
}
#Auth
subjects_url =  f"{BASE_URL}/api/{API_VERSION}/app/cdm/subjects?study_name={study_name}&study_country={study_country}&site={site}" 

# Send the GET request
retrieve_subjects = requests.get(subjects_url, headers=headers)

# Get the JSON response
json_response_retrieve_subjects = retrieve_subjects.json()

# Load JSON
#print(json.dumps(json_response_retrieve_subjects, indent=4))  # Prettify JSON

# Extract the 'subjects' key

subjects = [entry["subject"] for entry in json_response_retrieve_subjects["subjects"]]
# Define the URL and headers

#print(subjects)
payload = {
    "study_name": "HPC_Test_Study_DEV1",
    "eventgroups": []
}
for subject in subjects:
    payload["eventgroups"].extend([
        {
            "study_country": study_country,
            "site": site,
            "subject": subject,  # Placeholder for subject
            "eventgroup_name": "eg_TREATMENT",
            "eventgroup_sequence": "1"
        },
        {
            "study_country": study_country,
            "site": site,
            "subject": subject,  # Placeholder for subject
            "eventgroup_name": "eg_COMMON_FORMS",
            "eventgroup_sequence": "1",
            "date": "2020-03-03"
        },
        {
            "study_country": study_country,
            "site": site,
            "subject": subject,  # Placeholder for subject
            "eventgroup_name": "eg_EOS",
            "eventgroup_sequence": "1",
            "date": "2020-03-03"
        }
    ])

post_url = f"{BASE_URL}/api/{API_VERSION}/app/cdm/eventgroups"

print(json.dumps(payload, indent=4))  # Prettify JSON
    # Send the POST request
#response = requests.put(post_url, json=payload, headers=headers)
response = requests.put(post_url, data=json.dumps(payload), headers=headers)
    
    # Print the response for debugging
print(f"Subject: {subject}, Status Code: {response.status_code}, Response: {response.text}")
