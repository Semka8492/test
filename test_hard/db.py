from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///main.sqlite', echo=True, connect_args={'check_same_thread': False})
db = declarative_base()
db_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = db_Session()


class User(db):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    token = Column(String)
    counter = Column(Integer)

    def __repr__(self):
        return "<User(email='%s', token='%s', counter='%i')>" % (
            self.email, self.token, self.counter
        )


db.metadata.create_all(engine)

