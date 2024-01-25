from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

# create a declarative base class
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.chat_id

# define connection_string
connection_string = URL.create(
    "postgresql",
    username="koyeb-adm",
    password="5sMxyBD3Kchf",
    host="ep-mute-sky-92539008.eu-central-1.pg.koyeb.app",
    database="koyebdb",
)

# create engine
engine = create_engine(connection_string)

# create a scoped session
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# associate query property with the User class
User.query = db_session.query_property()


# define the shutdown_session function here
def shutdown_session(exception=None):
    db_session.remove()

def init_db():
    # import all modules here that might define models so they will
    # be registered properly on the metadata.  Otherwise you will have to
    # import them first before calling init_db()
    Base.metadata.create_all(bind=engine)