import requests
from bs4 import BeautifulSoup

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
   