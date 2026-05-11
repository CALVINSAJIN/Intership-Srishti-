from file_handler import load_users, save_users
from utils import encrypt_data, validate_password
from exceptions import UserAlreadyExistsError, AuthenticationError
from log import log_activity

def register_user(username, password):
    users = load_users()
    if username in users:
        raise UserAlreadyExistsError(f"User '{username}' already exists.")
    
    is_valid, msg = validate_password(password)
    if not is_valid:
        raise ValueError(msg)
    
    users[username] = encrypt_data(password)
    save_users(users)
    log_activity(username, "Registration Successful")
    return True

def authenticate_user(username, password):
    users = load_users()
    if username not in users or users[username] != encrypt_data(password):
        log_activity(username, "Login Failed")
        raise AuthenticationError("Invalid username or password.")
    
    log_activity(username, "Login Successful")
    return True