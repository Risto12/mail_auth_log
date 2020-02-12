from models import FilterAuthentications, DBTransactionHandler
from mail import Mail, MailContent
from conf_env import Config


class SendLogReport:

    @staticmethod
    def send_mail():
        db = DBTransactionHandler(Config.DB)
        log_report = FilterAuthentications(db)
        mail_content = MailContent(log_report)
        ready_mail = Mail(mail_content)
        ready_mail.send_mail()


class CheckLogs:

    @staticmethod
    def is_not_empty():
        db = DBTransactionHandler(Config.DB)
        log_report = FilterAuthentications(db)
        return log_report.usernames.__len__() != 0


if __name__ == '__main__':

    if CheckLogs.is_not_empty():
        SendLogReport.send_mail()

