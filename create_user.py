from auth import create_user

gestion_user = create_user(
    employee_number="11111",
    full_name="Gestion User",
    email="gestion@example.com",
    department="Gestion",
    password="password",
    role_name="gestion"
)
print(f"Gestion User created: {gestion_user.full_name}, Role: {gestion_user.role.name}")

commercial_user = create_user(
    employee_number="22222",
    full_name="Commercial User",
    email="commercial@example.com",
    department="Commercial",
    password="password",
    role_name="commercial"
)
print(f"Commercial User created: {commercial_user.full_name}, Role: {commercial_user.role.name}")

support_user = create_user(
    employee_number="33333",
    full_name="Support User",
    email="support@example.com",
    department="Support",
    password="password",
    role_name="support"
)
print(f"Support User created: {support_user.full_name}, Role: {support_user.role.name}")
