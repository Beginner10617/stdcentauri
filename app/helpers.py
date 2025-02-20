import requests, os, jwt
from bs4 import BeautifulSoup
from flask_mail import Message, Mail
from datetime import datetime, timedelta
from flask import url_for, render_template
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

mail = Mail()
load_dotenv()
WEBAPP_NAME = os.getenv('WEBAPP_NAME')
bcrypt = Bcrypt()

def get_student_details(ROLL_NUMBER):
    """
    Fetch student details from IITK OA website for the given roll number.
    :param ROLL_NUMBER: The roll number to fetch details for
    """
    # Start a session to maintain cookies
    s = requests.Session()

    # Step 1: Simulate visiting necessary pages to establish session
    s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Frameset.jsp")
    s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Intro.jsp?frm='SRCH'")
    s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITK_Srch.jsp?typ=stud")

    # Define headers (same as your working script)
    headers = {
        "Referer": "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchStudRoll_new.jsp"
    }

    # Define payload with roll number
    payload = {
        'typ': 'stud',  # Searching for students
        'numtxt': ROLL_NUMBER,  # The roll number to fetch
        'sbm': 'Y'
    }

    # Step 2: Send request to get details for the roll number
    response = s.post("https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchRes_new.jsp", headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract student details
        details = {}
        for para in soup.select('.TableContent p'):
            text = para.get_text().strip()
            if ":" in text:
                key, value = map(str.strip, text.split(":", 1))
                details[key] = value

        # Return extracted details
        if details:
            return details
        else:
            raise ValueError("No details found for the given roll number.")

    else:
        raise requests.RequestException(f"Failed to fetch details for roll number {ROLL_NUMBER}.")

def send_email(recipient, subject, body, cc=[]):
    """
    Send an email using the Flask-Mail extension.
    :param app: The Flask application instance
    :param recipient: The email address of the recipient
    :param subject: The subject of the email
    :param body: The body of the email
    """
    msg = Message(subject, recipients=[recipient], cc=cc, sender=os.getenv('EMAIL_ID'))
    msg.html = render_template('email.html', email_body=body, email_address=os.getenv('EMAIL_ID'))
    mail.send(msg)

def send_verification_email(user):
    token_for_verification = jwt.encode({'email': user.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, 'secret_key', algorithm='HS256')
    verify_url = url_for('routes.auth.verify_email', token=token_for_verification, _external=True)
    subject = 'Email Verification'
    body = '''
    Hi {name}!<br>
    To verify your email for {webapp_name}, visit the following link:<br>
    <a href="{verify_url}">{verify_url}</a><br>
    Please note that these links will expire in 24 hours.<br><br>
    If you did not create an account on {webapp_name}, please ignore this email, or check if someone else has used your email address to create an account.
    '''.format(name=user.name, webapp_name=WEBAPP_NAME, verify_url=verify_url)
    send_email(user.email, subject, body)
    