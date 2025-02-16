import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd
from datetime import datetime

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
# Read a comma-delimited .txt file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Move one directory level up
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Path to the CSV file
csv_file_path = os.path.join(parent_dir, '1234-5678_TEST_HPC_SU_FULL_2023FEB131011.txt')
df = pd.read_csv(csv_file_path , delimiter='|',dtype=str)  

# Rename columns while keeping original data intact
df = df.rename(columns={
    'Subject Number': 'subject', 
    'Tobacco Use':'SUNCF_TOBACCO',
    'Vaping Product':'SUNCF_VAP',
    'Alcohol Use':'SUNCF_ALC'
   
})



df = df.fillna("")
#df['CHILDPOT'] = df['CHILDPOT'].replace("", None).fillna("No")
#df["AGE"] = pd.to_numeric(df["AGE"], errors="coerce")

# prepare the data to be sent
json_payloads = []

for _, row in df.iterrows():
    subject = row['subject']  # Assuming the column name is 'subject'
  
    json_body = {
        "study_name": "HPC_Test_Study_DEV1",
        "reopen": True,
        "submit": True,
        "change_reason": "Updated by the integration",
        "externally_owned": True,
        "form": {
        "study_country": "Germany",
        "site": "DEU1",
        "subject": subject,
        "eventgroup_name": "eg_TREATMENT",
        "event_name": "ev_V01",
        "form_name": "SU_01_002",
        "itemgroups": [
            {
                "itemgroup_name": "ig_SU_01_002_A",
                "itemgroup_sequence": 1,
                "items": [
                    {
                        "item_name": "SUNCF_TOBACCO",
                        "value": row['SUNCF_TOBACCO']
                    },
                    {
                        "item_name": "SUNCF_VAP",
                        "value": row['SUNCF_VAP']
                    },
                     {
                        "item_name": "SUNCF_ALC",
                        "value": row['SUNCF_ALC']
                    }
                ]
            }
        ]                
    }
    }
    print(json.dumps(json_body, indent=4))
    json_payloads.append(json_body)


# Define the API endpoint

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {SESSION_ID}",  
}

api_endpoint =  f"{BASE_URL}/api/{API_VERSION}/app/cdm/forms/actions/setdata"
for payload in json_payloads:
    response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
    response_json = response.json()  # This directly parses the response if it's JSON
    print(json.dumps(response_json, indent=4))

