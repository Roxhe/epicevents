from database import SessionLocal, User, Role, Permission
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime
import os

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'OCP12SECRETKEY')


def create_jwt_token(user_id: int):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")


def create_role(name: str, description: str):
    db = SessionLocal()
    role = db.query(Role).filter(Role.name == name).first()
    if role is None:
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        db.refresh(role)
    db.close()
    return role


def create_permission(name: str, description: str):
    db = SessionLocal()
    permission = db.query(Permission).filter(Permission.name == name).first()
    if permission is None:
        permission = Permission(name=name, description=description)
        db.add(permission)
        db.commit()
        db.refresh(permission)
    db.close()
    return permission


def add_permission_to_role(role_name: str, permission_name: str):
    db = SessionLocal()
    role = db.query(Role).filter(Role.name == role_name).first()
    permission = db.query(Permission).filter(Permission.name == permission_name).first()
    if role and permission and permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()
    db.close()


def user_exists(email: str) -> bool:
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user is not None


def create_user(employee_number: str, full_name: str, email: str, department: str, password: str, role_name: str):
    if user_exists(email):
        raise ValueError(f"User with email {email} already exists")

    db = SessionLocal()
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role {role_name} does not exist")

    user = User(
        employee_number=employee_number,
        full_name=full_name,
        email=email,
        department=department,
        role_id=role.id
    )
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    user.role
    db.expunge(user)
    db.close()

    return user


def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        db.close()
        return None
    user.role.permissions
    db.expunge(user)
    db.close()
    return user


def has_permission(user: User, permission_name: str) -> bool:
    db = SessionLocal()
    permission = db.query(Permission).filter(Permission.name == permission_name).first()
    if permission:
        user = db.merge(user)
        if permission in user.role.permissions:
            db.close()
            return True
    db.close()
    return False
