from database import SessionLocal, Base, engine, Role, Permission
from auth import create_role, create_permission, add_permission_to_role

Base.metadata.create_all(bind=engine)


def get_or_create_role(name, description):
    db = SessionLocal()
    role = db.query(Role).filter(Role.name == name).first()
    if not role:
        role = create_role(name, description)
    db.close()
    return role


def get_or_create_permission(name, description):
    db = SessionLocal()
    permission = db.query(Permission).filter(Permission.name == name).first()
    if not permission:
        permission = create_permission(name, description)
    db.close()
    return permission


gestion_role = get_or_create_role("gestion", "Gestion user with full permissions")
commercial_role = get_or_create_role("commercial", "Commercial user with client and contract management permissions")
support_role = get_or_create_role("support", "Support user with event management permissions")

create_permission("create_user", "Permission to create users")
create_permission("update_user", "Permission to update users")
create_permission("delete_user", "Permission to delete users")
create_permission("create_contract", "Permission to create contracts")
create_permission("update_contract", "Permission to update contracts")
create_permission("create_event", "Permission to create events")
create_permission("update_event", "Permission to update events")
create_permission("view_all", "Permission to view all clients, contracts, and events")

add_permission_to_role("gestion", "create_user")
add_permission_to_role("gestion", "update_user")
add_permission_to_role("gestion", "delete_user")
add_permission_to_role("gestion", "create_contract")
add_permission_to_role("gestion", "update_contract")
add_permission_to_role("gestion", "create_event")
add_permission_to_role("gestion", "update_event")
add_permission_to_role("gestion", "view_all")

add_permission_to_role("commercial", "create_contract")
add_permission_to_role("commercial", "update_contract")
add_permission_to_role("commercial", "create_event")
add_permission_to_role("commercial", "view_all")

add_permission_to_role("support", "update_event")
add_permission_to_role("support", "view_all")

print("Database initialized with roles and permissions")
