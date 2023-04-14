# %%
from email.message import EmailMessage
import smtplib


def text_peter(subject, body):
    '''Send an email to Peter.
    
    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
    '''

    msg = EmailMessage()
    msg['subject'] = subject
    msg.set_content(body)
    msg['to'] = '5183449465@txt.att.net'

    user = 'mrpeterssyt@gmail.com'
    msg['from'] = user
    password = 'frjupscwijxfikib'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

# %%
import time
import requests
from bs4 import BeautifulSoup
import json
import warnings

warnings.filterwarnings("ignore")

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

dict_courses = {202410: [11817, 11818, 16991, 11850, 12097, 14421, 14422, 14432, 20014]}

while True:
    for terms, crns in dict_courses.items():
        for crn in crns:
            r = requests.get(f'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getEnrollmentInfo?term={terms}&courseReferenceNumber={crn}', verify=False)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                seats_available = soup.find_all('span')[5].text
                if int(seats_available) > 0:
                    r = requests.get(f'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getFacultyMeetingTimes?term={terms}&courseReferenceNumber={crn}', verify=False)
                    if r.status_code == 200:
                        # parse the json
                        json_data = json.loads(r.text)
                        # get the meeting times
                        meeting_time = json_data.get('fmt')[0].get('meetingTime')
                        start = meeting_time.get('beginTime')
                        end = meeting_time.get('endTime')
                        monday = meeting_time.get('monday')
                        tuesday = meeting_time.get('tuesday')
                        wednesday = meeting_time.get('wednesday')
                        thursday = meeting_time.get('thursday')
                        friday = meeting_time.get('friday')
                        saturday = meeting_time.get('saturday')
                        sunday = meeting_time.get('sunday')
                        # get prof
                        prof = json_data.get('fmt')[0].get('faculty')[0].get('displayName')

                        r = requests.get(f'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getClassDetails?term={terms}&courseReferenceNumber={crn}', verify=False)
                        soup = BeautifulSoup(r.text, 'html.parser')
                        course_name = soup.find("span", { "id" : "courseTitle" }).text
                        course_number = soup.find("span", { "id" : "courseNumber" }).text
                        subject = soup.find("span", { "id" : "subject" }).text

                        days_of_week = ''
                        if monday:
                            days_of_week += 'Monday, '
                        if tuesday:
                            days_of_week += 'Tuesday, '
                        if wednesday:
                            days_of_week += 'Wednesday, '
                        if thursday:
                            days_of_week += 'Thursday, '
                        if friday:
                            days_of_week += 'Friday, '
                        if saturday:
                            days_of_week += 'Saturday, '
                        if sunday:
                            days_of_week += 'Sunday, '

                        # send the text
                        text_peter(f'{course_name} is open!', f'Course {subject} {course_number} is open! It meets {days_of_week} from {start} to {end} and is taught by {prof}.')
                else:
                    print(f'{crn} is closed.')
            time.sleep(0.2)

    


