from models import FilterAuthentications, AuthLog, Base, Yesterday, DBTransactionHandler
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mail import MailContent
import unittest
from datetime import datetime, timedelta

test_db = 'sqlite:///test_db.db'


class MokDatabase:

    def __init__(self):
        self.engine = create_engine(test_db, echo=False)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.add_mok_data()

    def add_mok_data(self):
        self.add_authlog_today("Success", "tester1")
        self.add_authlog_today("Success", "tester1")
        self.add_authlog_today("Failure", "tester2")
        self.add_authlog_yesterday("Success", "tester1")
        self.add_authlog_yesterday("Success", "tester1")
        self.add_authlog_yesterday("Failure", "tester2")
        self.session.commit()

    def add_authlog_today(self, status, username):
        log_time = datetime.now()
        self.session.add(AuthLog(log_time=log_time, status=status, username=username, ip=None))

    def add_authlog_yesterday(self, status, username):
        log_time = datetime.now() - timedelta(1)
        self.session.add(AuthLog(log_time=log_time, status=status, username=username, ip=None))


class TestFilterAuthentications(unittest.TestCase):

    def setUp(self):
        MokDatabase()
        db_trans_handler = DBTransactionHandler(test_db)
        self.authentications = FilterAuthentications(db_trans_handler)

    def test_success(self):
        self.assertEqual(self.authentications.success, 2)

    def test_failures(self):
        self.assertEqual(self.authentications.failures, 1)

    def test_usernames_len(self):
        self.assertTrue(len(self.authentications.usernames), 2)

    def test_usernames_names(self):
        self.assertIn("tester1", self.authentications.usernames)
        self.assertIn("tester2", self.authentications.usernames)

    def test_attempts(self):
        self.assertEqual(self.authentications.attempts, 3)

    def tearDown(self):
        pass


class TestMailContent(unittest.TestCase):

    def setUp(self):
        MokDatabase()
        db_trans_handler = DBTransactionHandler(test_db)
        self.authentications = FilterAuthentications(db_trans_handler)
        self.mail_content = MailContent(self.authentications)

    def test_mail_content_text(self):
        self.assertIsNotNone(self.mail_content.get_text())

    def test_mail_content_html(self):
        self.assertIsNotNone(self.mail_content.get_html())

    def tearDown(self):
        pass


class TestYesterday(unittest.TestCase):

    def test_not_none(self):
        self.assertIsNotNone(Yesterday.get_yesterdays_date())

