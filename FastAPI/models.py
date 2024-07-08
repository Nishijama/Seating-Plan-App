from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Attendee(Base):
    __tablename__='attendees'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    family = Column(String)
    tier = Column(Integer)
    table = Column(Integer)
    so = Column(Integer)

