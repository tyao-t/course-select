from numpy import full
import requests
import smtplib

API_KEY = ""

term = "1231"
headers = {
    "x-api-key": API_KEY
}
message = ""
courses = []
send_email = False
full_message = ""
for course in courses:
    if (course == ""): continue
    subject = course.split(" ")[0]
    num = course.split(" ")[1]
    response = requests.get(f'https://openapi.data.uwaterloo.ca/v3/ClassSchedules/{term}/{subject}/{num}', headers = headers)
    assert response.status_code == 200
    r_data = response.json()
    full_message += f"{course}: \n"
    for entry in r_data:
        if (entry["courseComponent"] != "LEC") or (entry["sessionCode"] == "PCS"): 
            continue
        else:
            if entry['maxEnrollmentCapacity'] > entry['enrolledStudents']:
                full_message += f"Capacity: {str(entry['maxEnrollmentCapacity'])}, enrollment: {str(entry['enrolledStudents'])}\n"
                send_email = True

my_email = ""
my_password = ""
email_to = ""
smtp_server_address = "outlook.office365.com" 
if send_email:
    with smtplib.SMTP(smtp_server_address) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email_to,
            msg=f"Subject:Spaces available!\n\n{full_message}"
        )