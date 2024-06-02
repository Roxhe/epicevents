import getpass
import configparser
from auth import authenticate_user, create_jwt_token

email = input("Enter your email: ")
password = getpass.getpass("Enter your password: ")

user = authenticate_user(email, password)
if user:
    token = create_jwt_token(user.id)
    print(f"Authentication successful. Your token: {token}")

    config = configparser.ConfigParser()
    config['DEFAULT'] = {'JWT_TOKEN': token}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Token has been written to config.ini")
else:
    print("Authentication failed.")
