from auth import create_user

try:
    new_user = create_user(
        employee_number="11111",
        full_name="Ex Ample",
        email="Example@example.com",
        department="IT",
        password="password",
        role_name="gestion"
    )
    if new_user:
        print(f"User created: {new_user.full_name}, Role: {new_user.role.name}")
    else:
        print("Failed to create user.")
except ValueError as e:
    print(e)