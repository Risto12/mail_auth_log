import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf_env import Config
from models import FilterAuthentications, Yesterday


class MailContent:

    def __init__(self, filter_authentications: FilterAuthentications):
        self.log_statistics = filter_authentications

    def get_text(self):
        return """Date:{}\nattempts:{}\nsuccess:{}\nfailures:{}\nusernames:{}
        """.format(Yesterday.get_yesterdays_date(), self.log_statistics.attempts, self.log_statistics.success,
                   self.log_statistics.failures, self.log_statistics.usernames)

    def get_html(self):
        return """\
            <html>
                <body>
                    <h1>Date:{}</h1>
                    <p>attempts:{}</p>
                    <p>success:{}</p>
                    <p>failures:{}</p>
                    <p>usernames:{}</p>
                </body>
            </html>
        """.format(Yesterday.get_yesterdays_date(), self.log_statistics.attempts, self.log_statistics.success,
                   self.log_statistics.failures, self.log_statistics.usernames)


class Mail:

    def __init__(self, mail_content: MailContent):
        self._sender_email = Config.SENDER_EMAIL
        self._receiver_email = Config.RECEIVER_EMAIL
        self._password = Config.EMAIL_PASSWORD
        self._message = self.get_message(mail_content)

    def get_message(self, mail_content:MailContent):

        message = MIMEMultipart("alternative")
        message["Subject"] = "Log report"
        message["From"] = self._sender_email
        message["To"] = self._receiver_email
        part1 = MIMEText(mail_content.get_text(), "plain")
        part2 = MIMEText(mail_content.get_html(), "html")
        message.attach(part1)
        message.attach(part2)
        return message

    def send_mail(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(Config.GMAIL_SERVER, 465, context=context) as server:
            server.login(self._sender_email, self._password)
            server.sendmail(
                self._sender_email, self._receiver_email, self._message.as_string()
            )