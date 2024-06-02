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


def get_all_clients():
    db = SessionLocal()
    clients = db.query(Client).all()
    db.close()
    return clients


def get_all_contracts():
    db = SessionLocal()
    contracts = db.query(Contract).all()
    db.close()
    return contracts


def get_all_events():
    db = SessionLocal()
    events = db.query(Event).all()
    db.close()
    return events


def create_collaborator(employee_number, full_name, email, department, hashed_password, role_id):
    db = SessionLocal()
    new_user = User(
        employee_number=employee_number,
        full_name=full_name,
        email=email,
        department=department,
        hashed_password=hashed_password,
        role_id=role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


def update_collaborator(user_id, full_name=None, email=None, department=None, role_id=None):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return None
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if department:
        user.department = department
    if role_id:
        user.role_id = role_id
    db.commit()
    db.refresh(user)
    db.close()
    return user


def create_contract(client_id, commercial_contact, total_amount, amount_due, creation_date, status):
    db = SessionLocal()
    new_contract = Contract(
        client_id=client_id,
        commercial_contact=commercial_contact,
        total_amount=total_amount,
        amount_due=amount_due,
        creation_date=creation_date,
        status=status
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    db.close()
    return new_contract


def update_contract(contract_id, client_id=None, commercial_contact=None,
                    total_amount=None, amount_due=None, creation_date=None, status=None):
    db = SessionLocal()
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        db.close()
        return None
    if client_id:
        contract.client_id = client_id
    if commercial_contact:
        contract.commercial_contact = commercial_contact
    if total_amount:
        contract.total_amount = total_amount
    if amount_due:
        contract.amount_due = amount_due
    if creation_date:
        contract.creation_date = creation_date
    if status:
        contract.status = status
    db.commit()
    db.refresh(contract)
    db.close()
    return contract


def create_event(contract_id, client_name, client_contact, event_date_start,
                 event_date_end, support_contact, location, attendees, notes):
    db = SessionLocal()
    new_event = Event(
        contract_id=contract_id,
        client_name=client_name,
        client_contact=client_contact,
        event_date_start=event_date_start,
        event_date_end=event_date_end,
        support_contact=support_contact,
        location=location,
        attendees=attendees,
        notes=notes
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    db.close()
    return new_event


def update_event(event_id, contract_id=None, client_name=None, client_contact=None, event_date_start=None,
                 event_date_end=None, support_contact=None, location=None, attendees=None, notes=None):
    db = SessionLocal()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        db.close()
        return None
    if contract_id:
        event.contract_id = contract_id
    if client_name:
        event.client_name = client_name
    if client_contact:
        event.client_contact = client_contact
    if event_date_start:
        event.event_date_start = event_date_start
    if event_date_end:
        event.event_date_end = event_date_end
    if support_contact:
        event.support_contact = support_contact
    if location:
        event.location = location
    if attendees:
        event.attendees = attendees
    if notes:
        event.notes = notes
    db.commit()
    db.refresh(event)
    db.close()
    return event
