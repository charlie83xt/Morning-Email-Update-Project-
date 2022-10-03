import dd_content
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart
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
        

    def send_email(self):
        pass

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
            text += f' - {self.content["weather"]["content"]["Date"]} | {self.content["weather"]["content"]["Min Temperature"]}ºC | {self.content["weather"]["content"]["Description"]} - \n\n'
            text += f' - {self.content["weather"]["content"]["Wind Speed"]} | {self.content["weather"]["content"]["Max Temperature"]}ºC - '
        # format Twitter trends
        if self.content["twitter"]["include"] and self.content["twitter"]["content"]:
            text += f'*~*~* Top Ten Twitter Trends *~*~*\n\n'
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

        <h1>Daily Digest - {{datetime.date.today().strftime("%d %b %Y")}}</h1>
        """

        # format random quote
        if self.content["quote"]["include"] and self.content["quote"]["content"]:
            html += f"""
        <h2>Quote of the day</h2>
        <i>{self.content["quote"]["content"]}</i>
        """

        # format weather forecast
        if self.content["weather"]["include"] and self.content["weather"]["content"]:
            html += f"""
            <h2>Forecast for {self.content["weather"]["content"]["location"]}, {self.content["weather"]["content"]["country"]} is...</h2>
            <h3> {self.content["weather"]["content"]["Date"]} | {self.content["weather"]["content"]["Min Temperature"]}ºC | {self.content["weather"]["content"]["Description"]} </h3>
            <h3> {self.content["weather"]["content"]["Wind Speed"]} | {self.content["weather"]["content"]["Max Temperature"]}ºC </h3>
            """
        if self.content["twitter"]["include"] and self.content["twitter"]["content"]:
            html += f"""
            <h2>Tope Ten Twitter Trends</h2>
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
            <a target="_blank" href="{self.content["wikipedia"]["content"]["thumbnail"]}">
                <img src="{self.content["wikipedia"]["content"]["thumbnail"]}"></a>
            <h3>{self.content["wikipedia"]["content"]["content"]}</h3>
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