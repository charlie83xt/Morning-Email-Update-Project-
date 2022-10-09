import dd_content
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib
import os 
import datetime


live_pass = os.environ.get("HOTMAILPASS") #EMAIL SERVER ENV PASS

# Connection to email server
# smtp = smtplib.SMTP('smtp.live.com', 25)
# smtp.ehlo()
# smtp.starttls()

# Email login and Password
# smtp.login('charlie83xt@hotmail.com', live_pass)

class DailyDigestEmail:

    def __init__(self):
        self.content = {
            "quote":{"include":True, "content":dd_content.get_random_quote()},
            "weather":{"include":True, "content":dd_content.get_weather_forecast()},
            "twitter":{"include":True, "content":dd_content.get_twitter_trends()},
            "wikipedia":{"include":True, "content":dd_content.get_wikipedia_article()}
        }
    
        self.recipients_list = ["charlie83xt@yahoo.com", "menxu-1188@hotmail.com"]

        self.sender_credentials = {
            "email": 'charlie83xt@hotmail.com',
            "password": live_pass
        }

    def send_email(self):
        # Build email message
        msg = EmailMessage()
        msg['subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['from'] = self.sender_credentials['email']
        msg['to'] = ', '.join(self.recipients_list)

        # add plaintext in the body of message
        msg_body = self.format_message()
        msg.set_content(msg_body["text"])
        msg.add_alternative(msg_body["html"], subtype='html')

        # Secure connection with SMTP server and send email
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(self.sender_credentials['email'],
                         self.sender_credentials['password'])
            server.send_message(msg)
        
        """
        generate email message body as a plantext and HTML
        """

    def format_message(self):
        ###################
        ##Generating Text##
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'

        # format random quote
        if self.content["quote"]["include"] and self.content["quote"]["content"]:
            text += '*~*~*~*~* Quote of the day *~*~*~*~*\n\n'
            text += f'{self.content["quote"]["content"]}'
        # format weather forecast
        if self.content["weather"]["include"] and self.content["weather"]["content"]:
            text += f'*~*~*~*~* Forecast for {self.content["weather"]["content"]["location"]}, {self.content["weather"]["content"]["country"]} is... *~*~*~*~*\n\n'
            text += f' - {self.content["weather"]["content"]["Date"]} | Min {self.content["weather"]["content"]["Min Temperature"]}ºC | {self.content["weather"]["content"]["Description"]} - \n\n'
            text += f' - {self.content["weather"]["content"]["Wind Speed"]} | Max {self.content["weather"]["content"]["Max Temperature"]}ºC - \n\n'
        # format Twitter trends
        if self.content["twitter"]["include"] and self.content["twitter"]["content"]:
            text += f'*~*~* Top Ten Twitter Trends *~*~*\n'
            for trend in self.content["twitter"]["content"]:
                for inner_dict in trend["trends"][:10]:
                    text += f' - {inner_dict["name"]} : {inner_dict["url"]}\n'
                    text += "\n"
        # format wikipedia article
        if self.content["wikipedia"]["include"] and self.content["wikipedia"]["content"]:
            text += f' *~*~ Random Wikipedia Article ~*~*~*\n\n'
            text += f' {self.content["wikipedia"]["content"]["title"]}\n'
            text += f' {self.content["wikipedia"]["content"]["thumbnail"]}\n'
            text += f' {self.content["wikipedia"]["content"]["extract"]}\n'
            text += f' {self.content["wikipedia"]["content"]["content"]}\n'
        ###################
        ##Generating HTML##
        html = f"""<html>

    <body>
    <center>
    <meta charset="utf-8">
        <h1>Daily Digest - {datetime.date.today().strftime("%d %b %Y")}</h1>
        """

        # format random quote
        if self.content["quote"]["include"] and self.content["quote"]["content"]:
            html += f"""
        <h2>Quote of the day</h2>
        <p><em>{self.content["quote"]["content"]}</em></p>
        """

        # format weather forecast
        if self.content["weather"]["include"] and self.content["weather"]["content"]:
            html += f"""
            <h2>Forecast for {self.content["weather"]["content"]["location"]}, {self.content["weather"]["content"]["country"]} is...</h2>
            <h3> {self.content["weather"]["content"]["Date"]} | Min {self.content["weather"]["content"]["Min Temperature"]}ºC | {self.content["weather"]["content"]["Description"]} </h3>
            <h3> {self.content["weather"]["content"]["Wind Speed"]} | Max {self.content["weather"]["content"]["Max Temperature"]}ºC </h3>
            """
        if self.content["twitter"]["include"] and self.content["twitter"]["content"]:
            html += f"""
            <h2>Top Ten Twitter Trends</h2>
                    """
            for trend in self.content["twitter"]["content"]:
                for inner_dict in trend["trends"][:10]:
                    html += f"""
            <b><a href="{inner_dict["url"]}">{inner_dict["name"]}</a></b><p>
                    """
        # format wikipedia article
        if self.content["wikipedia"]["include"] and self.content["wikipedia"]["content"]:
            html += f"""
            <h2>Random Wikipedia Article</h2>
            <h2>{self.content["wikipedia"]["content"]["title"]}</h2>
            <a target="__blank" href="{self.content["wikipedia"]["content"]["thumbnail"]}">
            <img src="{self.content["wikipedia"]["content"]["thumbnail"]}" alt="{self.content["wikipedia"]["content"]["title"]}" width="200"></a>
            <br><a href="{self.content["wikipedia"]["content"]["content"]}">{self.content["wikipedia"]["content"]["title"]}</a>
            <table width="800">
                <tr>
                    <td>{self.content["wikipedia"]["content"]["extract"]}</td>
                </tr>
            </table>
                    """
            # footer
            html += f"""
    </center>
    </body>
</html>
                """
            return {"text": text, "html": html}

if __name__=='__main__':
    email = DailyDigestEmail()

    print('\nTesting email body generation...')
    message = email.format_message()

    # print Plaintext and HTML messages
    print('/nPlaintext email body is...')
    print(message['text'])
    print('\n--------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])

    # Save Plaintex and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])
    
    ### Test Send Email ###
    print('\n Sending test email...')
    email.send_email()