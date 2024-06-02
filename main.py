import os
import configparser
import argparse
from database import SessionLocal, Client, Contract, Event, User, get_all_clients, get_all_contracts, get_all_events
from auth import decode_jwt_token, has_permission

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

    if has_permission(user, "view_clients"):
        print("User has permission to view clients.")
        clients = get_all_clients()
        print("Clients:")
        for client in clients:
            print(f"{client.full_name}, {client.email}, {client.company_name}")
    else:
        print("User does not have permission to view clients.")

    if has_permission(user, "view_contracts"):
        print("User has permission to view contracts.")
        contracts = get_all_contracts()
        print("Contracts:")
        for contract in contracts:
            print(f"Contract {contract.id} for client {contract.client_id}, "
                  f"total amount: {contract.total_amount}, "
                  f"status: {contract.status}")
    else:
        print("User does not have permission to view contracts.")

    if has_permission(user, "view_events"):
        print("User has permission to view events.")
        events = get_all_events()
        print("Events:")
        for event in events:
            print(f"Event {event.id} for contract {event.contract_id}, "
                  f"location: {event.location}, "
                  f"date: {event.event_date_start} to {event.event_date_end}")
    else:
        print("User does not have permission to view events.")
except ValueError as e:
    print(e)
finally:
    db.close()
