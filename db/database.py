from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# data base engine
engine = create_engine('sqlite:///user.db')

# create basic class
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

# create table
Base.metadata.create_all(engine)

# create session, which connect with database
Session = sessionmaker(bind=engine)
session = Session()

