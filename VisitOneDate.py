import json
from dotenv import load_dotenv
import requests
import os
import pandas as pd
from datetime import datetime

load_dotenv()
#from CreateCasebookT import subjects

# Step 1: Load the CSV file into a DataFrame
# a: define varialbes and parameters 
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
SESSION_ID = os.getenv("SESSION_ID")
study_country = "Germany"  # Example country, change it as needed
study_name = 'HPC_Test_Study_DEV1'
site = 'DEU1'
eventgroup_name = 'eg_TREATMENT'
eventgroup_sequence = 1
event_name = 'ev_V01'



# b: define the headers 
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {SESSION_ID}",  
}

current_dir = os.path.dirname(os.path.abspath(__file__))

# Move one directory level up
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Path to the CSV file
csv_file_path = os.path.join(parent_dir, '1234-5678_TEST_HPC_VSTREAT_FULL_2024JUL101150.txt')

 # Update with  CSV file path
df = pd.read_csv(csv_file_path, delimiter='|',dtype=str)   

# Rename columns while keeping original data intact

df = df.rename(columns={
    'Subject Number': 'subject',  
    'Date of Measurement':'VSDAT'
})

def preprocess_dataframe(df):
    # Convert date format
    def convert_date_format(date_str):
        try:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return None  # Handle missing or invalid dates

    df["VSDAT"] = df["VSDAT"].apply(convert_date_format)
    return df
df = preprocess_dataframe(df)
# set the event date
#event_date = df['DSSTDAT_IC']
#event_date = str(df['DSSTDAT_IC'].iloc[0])
event_date = df['VSDAT'].tolist()

#print(type(event_date))
#print(event_date)
#subjects = subjects.tolist() if isinstance(subjects, pd.Series) else subjects
data = {
	"study_name": study_name,
    "events": [
        {
            "study_country": study_country,
            "site": site,
            "subject": row['subject'],
            "eventgroup_name": eventgroup_name,
            "eventgroup_sequence": eventgroup_sequence,
            "event_name": event_name,
            "date": row['VSDAT'],
            "change_reason": 'Subject creation'

        }
        for _, row in df.iterrows()
    ]
}

print(json.dumps(data, indent=4))



#Send the POST request

url =  f"{BASE_URL}/api/{API_VERSION}/app/cdm/events/actions/setdate"

post_setdate = requests.post(url, headers=headers, data=json.dumps(data))
response_json = post_setdate.json()  # This directly parses the response if it's JSON
print(json.dumps(response_json, indent=4))