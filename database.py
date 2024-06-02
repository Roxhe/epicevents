from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext

DATABASE_URL = "postgresql://crm_user:password@localhost/crm_db"

engine = create_engine(DATABASE_URL, connect_args={"options": "-csearch_path=public"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


role_permissions = Table('role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)


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
