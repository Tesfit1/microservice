import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd

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
csv_file_path = os.path.join(parent_dir, '1234-5678_TEST_HPC_DM_FULL_2023FEB131028.txt')
df = pd.read_csv(csv_file_path , delimiter='|',dtype=str)  

# Rename columns while keeping original data intact
df = df.rename(columns={
    'Subject Number': 'subject',  
    'Birth Year': 'BRTHDAT_YYYY',
    'Age':'AGE_2',
    'Sex':'SEX_2',
    'Child Bearing Potential':'CHILDPOT_1',
    'Gender':'GENIDENT',
    'Ethnicity':'ETHNIC',
    'American Indian or Alaska Native':'RACE_1',
    'Asian':'RACE_2',
    'Black or African American':'RACE_3',
    'Native Hawaiian or Other Pacific Islander':'RACE_4',
    'White':'RACE_5'

})
df = df.fillna("")
#df['CHILDPOT'] = df['CHILDPOT'].replace("", None).fillna("No")
#df["AGE"] = pd.to_numeric(df["AGE"], errors="coerce")

# prepare the data to be sent
json_payloads = []

for _, row in df.iterrows():
    subject = row['subject']  # Assuming the column name is 'subject'
    BRTHDAT_YYYY = row['BRTHDAT_YYYY']
    AGE = row['AGE_2']
    SEX = row['SEX_2']
    CHILDPOT = row['CHILDPOT_1']
    GENIDENT = row['GENIDENT']
    ETHNIC = row['ETHNIC']
    RACE_1 = row['RACE_1']
    RACE_2 = row['RACE_2']
    RACE_3 = row['RACE_3']
    RACE_4 = row['RACE_4']
    RACE_5 = row['RACE_5']
    json_body = {
        "study_name": "HPC_Test_Study_DEV1",
        "reopen": True,
        "submit": True,
        "change_reason": "Updated by the integration",
        "externally_owned": True,
        "form": {
            "study_country": study_country,
            "site": site,
            "subject": subject,
            "eventgroup_name": "eg_SCREEN",
            "event_name": "SUBJECT",
            "form_name": "DM_02_v001",
            "itemgroups": [
                {
                    "itemgroup_name": "ig_DM_02_A",
                    "itemgroup_sequence": 1,
                    "items": [
                        {
                            "item_name": "BRTHDAT_YYYY",
                            "value": BRTHDAT_YYYY
                        },
                        {
                            "item_name": "AGE_2",
                            "value": AGE
                        },
                        {
                            "item_name" : "SEX_2",
                            "value": SEX
                        },
                        {
                            "item_name" : "CHILDPOT_1",
                            "value": CHILDPOT
                        },
                        {
                            "item_name" : "GENIDENT",
                            "value": GENIDENT
                        },
                        {
                            "item_name" : "ETHNIC",
                            "value": ETHNIC
                        },
                         {
                            "item_name" : "RACE_1",
                            "value": RACE_1
                        },
                        {
                            "item_name" : "RACE_2",
                            "value": RACE_2
                        },
                        {
                            "item_name" : "RACE_3",
                            "value": RACE_3
                        },
                        {
                            "item_name" : "RACE_4",
                            "value": RACE_4
                        },
                        {
                            "item_name" : "RACE_5",
                            "value": RACE_5
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

