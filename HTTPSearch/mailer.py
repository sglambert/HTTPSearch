import smtplib
import textwrap
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configuration as config


class Mailer(object):

    def __init__(self):
        self.mail_sender = config.mail_sender
        self.mail_server = config.mail_server
        self.mail_port = config.mail_port


    def send_message(self, subject, html_body):
        msg = MIMEMultipart()

        recipients = config.recipients
        msg['subject'] = subject
        msg['from'] = self.mail_sender

        html = textwrap.dedent("""
            <html>
            <body>
            %s
            </body>
            </html>
        """)
        part = MIMEText(html % html_body, 'html', 'utf-8')
        msg.attach(part)

        smtpServer = smtplib.SMTP(self.mail_server, self.mail_port)
        smtpServer.ehlo()
        smtpServer.starttls()
        smtpServer.login(self.mail_sender, config.app_password)
        smtpServer.sendmail(self.mail_sender, recipients, msg.as_string())
        smtpServer.quit()
