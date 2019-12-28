# coding: utf-8
from sqlalchemy import create_engine, Column, DateTime, String, Text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()
metadata = Base.metadata


class AuthLog(Base):
    __tablename__ = 'auth_log'

    status_types = ('Success', 'Failure')

    id = Column(INTEGER(11), primary_key=True)
    log_time = Column(DateTime)
    status = Column(String(64))
    ip = Column(String(64))
    username = Column(String(64))


class Yesterday:

    @staticmethod
    def get_yesterdays_date():
        return datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')


class DBConnection:

    def __init__(self, engine):
        engine = create_engine(engine, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()


class DBTransactionHandler(DBConnection):

    def __init__(self, engine, query_date=Yesterday.get_yesterdays_date()):
        super().__init__(engine)
        self.query_date = query_date

    def get_auth_log(self):
        auth_log = self.session.query(AuthLog).filter(AuthLog.log_time.like(self.query_date + "%")).all()
        return auth_log


class FilterAuthentications:

    def __init__(self, db_transaction_handler):
        self.db = db_transaction_handler
        self.attempts = 0
        self.success = 0
        self.failures = 0
        self.usernames = []
        self._populate_attributes()

    def _populate_attributes(self):
        self._count_success()
        self._count_failures()
        self._count_attempts()
        self._get_usernames()

    def _count_success(self):
        for auth in self.db.get_auth_log():
            if auth.status == "Success":
                self.success += 1

    def _count_failures(self):
        for auth in self.db.get_auth_log():
            if auth.status == "Failure":
                self.failures += 1

    def _count_attempts(self):
        self.attempts = len(self.db.get_auth_log())

    def _get_usernames(self):
        for auth in self.db.get_auth_log():
            if auth.username not in self.usernames:
                self.usernames.append(auth.username)

    def __str__(self):
        return "There is {} attempts\n{} success\n{} failures\n{} usernames".format(self.attempts,
                                                                                    self.success,
                                                                                    self.failures,
                                                                                    self.usernames)




