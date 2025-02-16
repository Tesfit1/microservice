import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Variables
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
SESSION_ID = os.getenv("SESSION_ID")
study_country = "Germany"
study_name = 'HPC_Test_Study_DEV1'
site = 'DEU1'

# Read a comma-delimited .txt file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
csv_file_path = os.path.join(parent_dir, '1234-5678_TEST_HPC_SAMP_TPT_PK_FULL_2022FEB171150.txt')
df = pd.read_csv(csv_file_path, delimiter='|', dtype=str)

# Rename columns while keeping original data intact
df = df.rename(columns={
    'Subject Number': 'subject',
    'Time Point': 'TPT_TPT',
    'Sample Date': 'DAT_TPT',
    'Sample Time': 'TIM_TPT',
    'Comment': 'COM_TPT'
})

def preprocess_dataframe(df):
    def convert_date_format(date_str):
        try:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return None

    df["DAT_TPT"] = df["DAT_TPT"].apply(convert_date_format)
    return df

df = preprocess_dataframe(df)
df = df.fillna("")

# Prepare JSON payloads
json_payloads = []
current_subject = None  # Track current subject
itemgroup_sequence = 1  # Start sequence counter

for _, row in df.iterrows():
    subject = row['subject']

    # Reset itemgroup_sequence if subject changes
    if subject != current_subject:
        current_subject = subject
        itemgroup_sequence = 1

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
            "eventgroup_name": "eg_TREATMENT",
            "event_name": "ev_V01",
            "form_name": "SAMP_TPT_01_v001",
            "itemgroups": [
                {
                    "itemgroup_name": "ig_SAMP_TPT_01_A",
                    "itemgroup_sequence": itemgroup_sequence,
                    "items": [
                        {
                            "item_name": "TPT_TPT",
                            "value": row['TPT_TPT']
                        },
                        {
                            "item_name": "DAT_TPT",
                            "value": row['DAT_TPT']
                        },
                        {
                            "item_name": "TIM_TPT",
                            "value": row['TIM_TPT']
                        },
                        {
                            "item_name": "COM_TPT",
                            "value": row['COM_TPT']
                        }
                    ]
                }
            ]
        }
    }
    json_payloads.append(json_body)
    itemgroup_sequence += 1  # Increment sequence for the next event

    # Optional: Print JSON for debugging
    print(json.dumps(json_body, indent=4))

# Define the API endpoint
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {SESSION_ID}",
}

api_endpoint = f"{BASE_URL}/api/{API_VERSION}/app/cdm/forms/actions/setdata"

# Send JSON payloads to the API
for payload in json_payloads:
    response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
    response_json = response.json()  # Parse response if it's JSON
    print(json.dumps(response_json, indent=4))
