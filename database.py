from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql://crm_user:password@localhost/crm_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_nb = Column(String)
    company_name = Column(String)
    first_contact_date = Column(Date)
    last_contact_date = Column(Date)
    commercial_contact = Column(String)


class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    commercial_contact = Column(String)
    total_amount = Column(Float)
    amount_due = Column(Float)
    creation_date = Column(Date)
    status = Column(String)
    client = relationship("Client", back_populates="contracts")


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    client_name = Column(String)
    client_contact = Column(String)
    event_date_start = Column(Date)
    event_date_end = Column(Date)
    support_contact = Column(String)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)
    contract = relationship("Contract", back_populates="events")


Client.contracts = relationship("Contract", order_by=Contract.id, back_populates="client")
Contract.events = relationship("Event", order_by=Event.id, back_populates="contract")

Base.metadata.create_all(bind=engine)
