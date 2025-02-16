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
csv_file_path = os.path.join(parent_dir, '1234-5678_TEST_HPC_VSSCR_FULL_2024JUL101140.txt')
df = pd.read_csv(csv_file_path , delimiter='|',dtype=str)  

# Rename columns while keeping original data intact
df = df.rename(columns={
    'Subject Number': 'subject', 
    'Date of Measurement':'VSDAT_1',
    'Time of Measurement':'VSTIM',
    'Height':'HEIGHT_1',
    'Weight' :'WEIGHT_1',
    'Pulse Rate':'PULSE_1',
    'Systolic Blood Pressure':'SYSBP_1',
    'Diastolic Blood Pressure':'DIABP_1',
    'Respiratory Rate':'RESP_1',
    'Temperature':'TEMP_1'
})

def preprocess_dataframe(df):
    # Convert date format
    def convert_date_format(date_str):
        try:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return None  # Handle missing or invalid dates

    df["VSDAT_1"] = df["VSDAT_1"].apply(convert_date_format)
    return df
df = preprocess_dataframe(df)
# set the event date
#event_date = df['DSSTDAT_IC']
#event_date = str(df['DSSTDAT_IC'].iloc[0])


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
            "study_country": study_country,
            "site": site,
            "subject": subject,
            "eventgroup_name": "eg_SCREEN",
            "event_name": "ev_In-ExEligibility",
            "form_name": "VS_01_SCR",
            "itemgroups": [
            {
                "itemgroup_name": "ig_VS_01_A_SCR",
                "itemgroup_sequence": 1,
                "items": [
                    {
                        "item_name": "VSDAT_1",
                        "value": row['VSDAT_1']
                    },
                    {
                        "item_name": "VSTIM",
                        "value": row['VSTIM']
                    },
                     {
                        "item_name": "HEIGHT_1",
                        "value": row['HEIGHT_1'],
                        "unit_value":"Centimeter"
                    },
                    {
                        "item_name":"WEIGHT_1",
                        "value": row['WEIGHT_1'],
                        "unit_value":"Kilogram"
                    },
                    {
                        "item_name" : "PULSE_1",
                        "value": row['PULSE_1'],
                        "unit_value":"Beats-per-Minute"
                    },
                    {
                        "item_name" : "SYSBP_1",
                        "value": row['SYSBP_1'],
                        "unit_value":"mmHG"
                    },
                    {
                        "item_name" : "DIABP_1",
                        "value": row['DIABP_1'],
                        "unit_value":"mmHG"
                    },
                    {
                        "item_name" : "RESP_1",
                        "value": row['RESP_1'],
                        "unit_value":"Breaths-per-Minute"
                    },
                    {
                        "item_name" : "TEMP_1",
                        "value": row['TEMP_1'],
                        "unit_value":"Degree-Celsius"
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

