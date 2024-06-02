import os
import configparser
import argparse
from datetime import date
from database import SessionLocal, User, Role, Client, create_contract, update_contract, create_event, update_event, \
    update_collaborator
from auth import decode_jwt_token, has_permission, create_user

parser = argparse.ArgumentParser(description="Epicevents Script")
parser.add_argument('--token', type=str, help="JWT token to use for authentication")
args = parser.parse_args()

if args.token:
    token = args.token
else:
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['DEFAULT'].get('JWT_TOKEN')

if not token:
    print("No JWT token found. Please authenticate first.")
    exit()

try:
    user_id = decode_jwt_token(token)
    print(f"Authenticated user ID: {user_id}")

    db = SessionLocal()
    user = db.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    print(f"Authenticated user: {user.full_name}")

    if has_permission(user, "create_user"):
        new_collaborator = create_user(
            employee_number="44444",
            full_name="New Collaborator",
            email="newcollab@example.com",
            department="Sales",
            password="password_example",
            role_name="commercial"
        )
        print(f"Created Collaborator: ID: {new_collaborator.id}, Employee Number: {new_collaborator.employee_number}, "
              f"Full Name: {new_collaborator.full_name}, Email: {new_collaborator.email}, "
              f"Department: {new_collaborator.department}, Role: {new_collaborator.role.name}")

    if has_permission(user, "update_user"):
        role = db.query(Role).filter(Role.name == "support").first()
        if not role:
            raise ValueError("Role not found")

        updated_collaborator = update_collaborator(
            user_id=new_collaborator.id,
            full_name="Updated Collaborator",
            email="updatedcollab@example.com",
            department="Marketing",
            role_id=role.id
        )

        updated_collaborator = db.get(User, updated_collaborator.id)
        print(f"Updated Collaborator: ID: {updated_collaborator.id}, "
              f"Employee Number: {updated_collaborator.employee_number}, Full Name: {updated_collaborator.full_name}, "
              f"Email: {updated_collaborator.email}, Department: {updated_collaborator.department}, "
              f"Role: {updated_collaborator.role.name}")

    if has_permission(user, "create_contract"):
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
        print(f"Created Client: ID: {new_client.id}, Full Name: {new_client.full_name}, Email: {new_client.email}, "
              f"Phone: {new_client.phone_nb}, Company Name: {new_client.company_name}, "
              f"First Contact Date: {new_client.first_contact_date}, Last Contact Date: {new_client.last_contact_date},"
              f" Commercial Contact: {new_client.commercial_contact}")

        new_contract = create_contract(
            client_id=new_client.id,
            commercial_contact=new_client.commercial_contact,
            total_amount=20000.0,
            amount_due=10000.0,
            creation_date=date.today(),
            status="Pending"
        )
        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)
        print(f"Created Contract: ID: {new_contract.id}, Client ID: {new_contract.client_id}, "
              f"Commercial Contact: {new_contract.commercial_contact}, Total Amount: {new_contract.total_amount}, "
              f"Amount Due: {new_contract.amount_due}, Creation Date: {new_contract.creation_date}, "
              f"Status: {new_contract.status}")

    if has_permission(user, "update_contract"):
        updated_contract = update_contract(
            contract_id=new_contract.id,
            status="Signed"
        )
        print(f"Updated Contract: ID: {updated_contract.id}, Client ID: {updated_contract.client_id}, "
              f"Commercial Contact: {updated_contract.commercial_contact}, "
              f"Total Amount: {updated_contract.total_amount}, Amount Due: {updated_contract.amount_due}, "
              f"Creation Date: {updated_contract.creation_date}, Status: {updated_contract.status}")

    if has_permission(user, "create_event"):
        new_event = create_event(
            contract_id=new_contract.id,
            client_name=new_client.full_name,
            client_contact=new_client.email,
            event_date_start=date(2023, 6, 4),
            event_date_end=date(2023, 6, 5),
            support_contact="Support Contact",
            location="Event Location",
            attendees=100,
            notes="Event Notes"
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        print(f"Created Event: ID: {new_event.id}, Contract ID: {new_event.contract_id}, Client Name: {new_event.client_name}, Client Contact: {new_event.client_contact}, Event Start Date: {new_event.event_date_start}, Event End Date: {new_event.event_date_end}, Support Contact: {new_event.support_contact}, Location: {new_event.location}, Attendees: {new_event.attendees}, Notes: {new_event.notes}")

    if has_permission(user, "update_event"):
        updated_event = update_event(
            event_id=new_event.id,
            notes="Updated Event Notes"
        )
        print(f"Updated Event: ID: {updated_event.id}, Contract ID: {updated_event.contract_id}, Client Name: {updated_event.client_name}, Client Contact: {updated_event.client_contact}, Event Start Date: {updated_event.event_date_start}, Event End Date: {updated_event.event_date_end}, Support Contact: {updated_event.support_contact}, Location: {updated_event.location}, Attendees: {updated_event.attendees}, Notes: {updated_event.notes}")

except ValueError as e:
    print(e)
finally:
    db.close()
