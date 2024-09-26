from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import de_content

<<<<<<< HEAD
=======
# --- Email Credential Config ---

import os
import pickle
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

sender_email = "matt.emaildigest@gmail.com"
# -------------------------------

>>>>>>> de38161 (email now sends | added github secrets)
class Email:
    def __init__(self):
        self.message = MIMEMultipart("alternative")
        self.message["From"] = None # TODO
        self.message["To"] = "m.latinomain@icloud.com" # TODO
        weekday_name = datetime.now().strftime("%A")
        date_num = datetime.now().day
        month_name = datetime.now().strftime("%B")
        year = datetime.now().strftime("%Y")
        self.message["Subject"] = f"Daily Digest - {weekday_name} {date_num} {month_name} {year}"

        self.data = {
            "forecast": de_content.get_forecast(),
            "events": de_content.get_events(),
            "finance": de_content.get_finance()
        }
    def format_message(self):
        part1 = MIMEText(self.__generate_plaintext(), "plain")
        part2 = MIMEText(self.__generate_html(), 'html')
        return self.__generate_html() # delete after tested

    def send_email(self):
<<<<<<< HEAD
        pass
=======
        self.format_message()
        creds = self.__authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)

        raw_message = base64.urlsafe_b64encode(self.message.as_bytes()).decode()

        try:
            service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    

    def __authenticate_gmail(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is created automatically
        # when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'{os.getenv('GOOGLE_ID')}.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds


# If modifying these SCOPES, delete the file token.pickle.


>>>>>>> de38161 (email now sends | added github secrets)

    def __generate_plaintext(self):
        intro_text = """\
DAILY DIGEST

Good Morning!
Here is your daily digest for today!\n\n"""

        forecast_text = self.__forecast_to_text()

        events_text = self.__event_to_text()

        finance_text = self.__finance_to_text()

        plaintext_message = intro_text + forecast_text + events_text + finance_text

        return plaintext_message

    def __forecast_to_text(self):
        output = f"""### FORECAST ###
The forecast today in {self.data['forecast']['city']} is as follows:\n"""
        for period in self.data['forecast']['periods']:
            output += f"~ {period['time']} ~\n"
            output += f"{period['status']} - {period['temp']} celcius\n\n"
        return output

    def __event_to_text(self):
        output = "### EVENTS ###\n"
        if len(self.data['events']) == 0:
            output += "No Events Today!\n\n"
            return output
        for event in self.data['events']:
            output += f"-- {event['name']} --\n"
            output += f"From {event['start_time']} until {event['end_time']}\n\n"
        return output
            
    def __finance_to_text(self):
        return f"""### FINANCE ###
Net Worth: {self.data['finance']['net_worth']}
Budget Used: {self.data['finance']['budget_used']}
Balance Left: {self.data['finance']['balance']}\n"""

    def __generate_html(self):
        output = f"""
        <html>
            <head>
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <h1>Daily Digest</h1>
                <p>Today's Date: {datetime.now().strftime("%d/%m/%Y")}</p>
                <p>Your daily digest is as follows:</p>

                <h2>Forecast</h2>
                {self.__forecast_to_html()}

                <h2>Events</h2>
                {self.__event_to_html()}

                <h2>Finance</h2>
                {self.__finance_to_html()}
            </body>
        </html>"""
        return output

    def __forecast_to_html(self):
        icon_url = "http://openweathermap.org/img/wn/"
        output = "<div id='forecast'>"
        output += f"<p> 24-Hour Forecast in <b>{self.data['forecast']['city']}</b></p>"
        for period in self.data['forecast']['periods']:
            output += f"""<div class='period'>
    <h4>{period['time']} <img src='{icon_url+period['weather_icon']+".png"}' alt='{period['status'].upper()}'></h4>
    <p>{period['temp']}&deg;C</p>
    </div>
    """
        output += "</div>"
        return output

    def __event_to_html(self):
        output = "<div class='events'>"
        if len(self.data['events'])==0:
            output += "<p>No events today!"
        else:
            for event in self.data['events']:
                output += f"""<h3>{event['name']}</h3>
                <p>{event['start_time']} - {event['end_time']}<p>"""
        output += "</div>"
        return output

    def __finance_to_html(self):
        return f"""<div class='finance'>
        <ul>
            <li><b>Current Net Worth:</b> {self.data['finance']['net_worth']}</li>
            <li><b>Monthly Budget Used:</b> {self.data['finance']['budget_used']}</li>
            <li><b>Balance Left:</b> {self.data['finance']['balance']}</li>
        <ul>
        </div>"""


if __name__ == "__main__":
    email_msg = Email()
    with open("html_message.html", 'w') as file:
        file.write(email_msg.format_message())