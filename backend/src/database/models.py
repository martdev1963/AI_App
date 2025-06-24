from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Generator

#---------------------------------------------------------------------------------------------
# vid_time: 1:28:00 / 2:31:54
# ORM:
# Python wrappers called object relational mapping
# If you already have .env files tracked by git, you’ll need to untrack them
# git rm --cached .env
#---------------------------------------------------------------------------------------------
'''
----------------------------------------------------------------------------------------------
sqlite - Its a local database setup on our own computer.
ITs just a file that's automatically created. If you wanted to connect to
a remote database, like a MySQL database or you're hosting it in the cloud or something
then you would have to set the database connection string path here to connect to it:
engine = create_engine('sqlite:///database.db', echo=True)
----------------------------------------------------------------------------------------------
'''

# local string from our local machine for sqlite
# engine represents the database object...
engine = create_engine('sqlite:///database.db', echo=True)

# ORM Base class
Base = declarative_base()

# inheriting from ORM Base class
class Challenge(Base):
    __tablename__ = 'challenges'
    # establish table columns for data model 1
    id = Column(Integer, primary_key=True)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    created_by = Column(String, nullable=False) # the linkage to our user and the challenge created by him
    title = Column(String, nullable=False)
    options = Column(String, nullable=False) # option 1, option 2, etc...
    correct_answer_id = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)

   # For debugging/logging purposes, it's helpful
   # This gives you readable output when printing instances or logging
   # Handy for debugging or any dev sanity checks.
    def __repr__(self):
        return f"<Challenge(id={self.id}, title='{self.title}', difficulty='{self.difficulty}')>"


# establish table columns for data model 2
# #(challenge quota - limit on how many challenges generated per day per user)
class ChallengeQuota(Base):
    __tablename__ = 'challenge_quotas'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, default=datetime.now)

    # For debugging/logging purposes, it's helpful
    # This gives you readable output when printing instances or logging
    # Handy for debugging or any dev sanity checks.
    def __repr__(self):
        return f"<ChallengeQuota(user_id={self.user_id}, quota_remaining={self.quota_remaining})>"


# convert these data models written in python into SQL code...
Base.metadata.create_all(engine)

# this session represents are database connection...
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a database session (This type of function is called a generator)
# get_db() is a proper generator for dependency injection in frameworks like FastAPI
def get_db():
    db = SessionLocal() # this is one single connection to our database...we will yield the same connection everytime...
    try:
        yield db   # avoids creating duplicate sessions of our database...due to every session is a different connection...
    finally:
        db.close()
