from flask import Flask, jsonify
import subprocess
import logging 
import schedule
import time

app = Flask(__name__)

@app.route('/run-code', methods=['GET'])
    # Run the external Python script
def batch_loading():
    scripts = ["AuthT.py", "CreateCasebookT.py", "Subject_Ev_Date.py","subject.py","Event_DM_T.py","visitzero.py","IC_Ev_Date.py","Event_IC_T.py","SetEventEx_In_Elig.py","VitalSignScreening.py","Inc_Ex.py","Eligibility.py","Eventgroups.py","VisitOneDate.py","SamplingTimePoints.py","DrugAdmin.py","SubstanceUse.py","VitalSignvisitoneTreatment.py","SetEventDateEndOfStudy.py","EndOfTreatment.py"]
    python_path = r"C:\Users\tesfi\Documents\HPC\myenv\Scripts\python.exe"
    for script in scripts:
        try:
            subprocess.run([python_path, script], check=True)
            log_message(f"{script} executed successfully")
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing {script}: {e}", level='error')

if __name__ == '__main__':
    app.run(debug=True)
def log_message(message, level='info'):
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)

            #send_email("Batch Loading Error", f"Error executing {script}: {e}")

# Schedule the batch loading
# schedule.every().day.at("09:59").do(batch_loading)

# Keep the script running
# while True:
#     schedule.run_pending()
#     time.sleep(1)