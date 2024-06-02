from datetime import date
from database import SessionLocal, Client, Contract, Event
from auth import authenticate_user, has_permission

db = SessionLocal()

authenticated_user = authenticate_user("Example@example.com", "password")
if authenticated_user:
    print(f"Authenticated user: {authenticated_user.full_name}, Role: {authenticated_user.role.name}")
else:
    print("Failed to authenticate user")

if authenticated_user and has_permission(authenticated_user, "create_user"):
    new_client = Client(
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone_nb="+678 123 456 78",
        company_name="Cool Startup LLC",
        first_contact_date=date(2021, 4, 18),
        last_contact_date=date(2023, 3, 29),
        commercial_contact="Bill Boquet"
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    new_contract = Contract(
        client_id=new_client.id,
        commercial_contact=new_client.commercial_contact,
        total_amount=10000.0,
        amount_due=5000.0,
        creation_date=date(2023, 3, 29),
        status="Signed"
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)

    new_event = Event(
        contract_id=new_contract.id,
        client_name=new_client.full_name,
        client_contact=new_client.email,
        event_date_start=date(2023, 6, 4),
        event_date_end=date(2023, 6, 5),
        support_contact="Kate Hastroff",
        location="53 Rue du Château, 41120 Candé-sur-Beuvron, France",
        attendees=75,
        notes="Wedding starts at 3PM, by the river. Catering is organized, reception starts at 5PM. Kate needs to organize the DJ for after party."
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    print(f"Client: {new_client.full_name}, Email: {new_client.email}")
    print(f"Contract: {new_contract.total_amount}, Status: {new_contract.status}")
    print(f"Event: {new_event.client_name}, Location: {new_event.location}")
else:
    print("User does not have permission to create a user.")

db.close()
