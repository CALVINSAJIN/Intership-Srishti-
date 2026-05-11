import base64
import re

def encrypt_data(data):
    """Bonus: Basic base64 encryption for passwords."""
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encoded_data):
    """Decodes base64 strings."""
    return base64.b64decode(encoded_data.encode()).decode()

def validate_password(password):
    """Bonus: Validates password strength."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one digit."
    return True, ""