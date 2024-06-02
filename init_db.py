from database import SessionLocal, Role, Permission


def create_role(name, description):
    db = SessionLocal()
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    db.close()
    return role


def create_permission(name, description):
    db = SessionLocal()
    permission = Permission(name=name, description=description)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    db.close()
    return permission


gestion_role = create_role("gestion", "Gestion user with full permissions")
commercial_role = create_role("commercial", "Commercial user with client-specific permissions")
support_role = create_role("support", "Support user with event-specific permissions")

view_clients_perm = create_permission("view_clients", "View clients")
view_contracts_perm = create_permission("view_contracts", "View contracts")
view_events_perm = create_permission("view_events", "View events")
create_user_perm = create_permission("create_user", "Create users")
create_contract_perm = create_permission("create_contract", "Create contracts")
create_event_perm = create_permission("create_event", "Create events")
update_user_perm = create_permission("update_user", "Update users")
delete_user_perm = create_permission("delete_user", "Delete users")
update_contract_perm = create_permission("update_contract", "Update contracts")
delete_contract_perm = create_permission("delete_contract", "Delete contracts")
update_event_perm = create_permission("update_event", "Update events")
delete_event_perm = create_permission("delete_event", "Delete events")

create_client_perm = create_permission("create_client", "Create clients")
update_own_client_perm = create_permission("update_own_client", "Update own clients")
update_own_contract_perm = create_permission("update_own_contract", "Update own contracts")

update_assigned_event_perm = create_permission("update_assigned_event", "Update assigned events")

db = SessionLocal()

gestion_role = db.query(Role).filter(Role.name == "gestion").first()
gestion_permissions = [view_clients_perm, view_contracts_perm, view_events_perm,
                       create_user_perm, create_contract_perm, create_event_perm,
                       update_user_perm, delete_user_perm, update_contract_perm,
                       delete_contract_perm, update_event_perm, delete_event_perm]
for perm in gestion_permissions:
    if perm not in gestion_role.permissions:
        gestion_role.permissions.append(perm)

commercial_role = db.query(Role).filter(Role.name == "commercial").first()
commercial_permissions = [view_clients_perm, view_contracts_perm, view_events_perm,
                          create_client_perm, update_own_client_perm, update_own_contract_perm,
                          create_event_perm]
for perm in commercial_permissions:
    if perm not in commercial_role.permissions:
        commercial_role.permissions.append(perm)

support_role = db.query(Role).filter(Role.name == "support").first()
support_permissions = [view_events_perm, update_assigned_event_perm]
for perm in support_permissions:
    if perm not in support_role.permissions:
        support_role.permissions.append(perm)

db.commit()
db.close()

print("Roles and permissions have been created and associated successfully.")
