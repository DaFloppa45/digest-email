from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import de_content

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
        intro_text = """\
DAILY DIGEST

Good Morning!
Here is your daily digest for today!\n\n"""

        forecast_text = self.__forecast_to_text()

        events_text = self.__event_to_text()

        finance_text = self.__finance_to_text()

        plaintext_message = intro_text + forecast_text + events_text + finance_text

        return plaintext_message

    def send_email(self):
        pass

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



if __name__ == "__main__":
    email_msg = Email()
    print(email_msg.format_message())