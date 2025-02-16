import schedule
import time
import subprocess
import logging 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Logging setup
logging.basicConfig(filename='batch_loading.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def log_message(message, level='info'):
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)

# Email notification setup
# def send_email(subject, body):
#     sender_email = "your_email@example.com"
#     receiver_email = "receiver_email@example.com"
#     password = "solabelag"

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP('smtp.example.com', 587)
#         server.starttls()
#         server.login(sender_email, password)
#         text = msg.as_string()
#         server.sendmail(sender_email, receiver_email, text)
#         server.quit()
#         log_message("Email sent successfully")
#     except Exception as e:
#         log_message(f"Failed to send email: {e}", level='error')

# Batch loading function
def batch_loading():
    scripts = ["AuthT.py", "CreateCasebookT.py", "Subject_Ev_Date.py","subject.py","Event_DM_T.py","visitzero.py","IC_Ev_Date.py","Event_IC_T.py","SetEventEx_In_Elig.py","VitalSignScreening.py","Inc_Ex.py","Eligibility.py","Eventgroups.py","VisitOneDate.py","SamplingTimePoints.py","DrugAdmin.py","SubstanceUse.py","VitalSignvisitoneTreatment.py","SetEventDateEndOfStudy.py","EndOfTreatment.py"]
    python_path = r"C:\Users\tesfi\Documents\HPC\myenv\Scripts\python.exe"
    for script in scripts:
        try:
            subprocess.run([python_path, script], check=True)
            log_message(f"{script} executed successfully")
        except subprocess.CalledProcessError as e:
            log_message(f"Error executing {script}: {e}", level='error')
            #send_email("Batch Loading Error", f"Error executing {script}: {e}")

# Schedule the batch loading
schedule.every().day.at("09:59").do(batch_loading)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)