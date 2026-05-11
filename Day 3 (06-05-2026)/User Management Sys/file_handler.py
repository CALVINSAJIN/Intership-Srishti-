import csv
import os
import shutil

DB_FILE = "users.csv"

def load_users():
    """Reads the user database from a CSV file."""
    if not os.path.exists(DB_FILE):
        return {}
    users = {}
    try:
        with open(DB_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[row['username']] = row['password']
        return users
    except (IOError, KeyError):
        return {}

def save_users(users):
    """Writes user data to a CSV file and creates a backup."""
    create_backup()  # Bonus: File backup system
    with open(DB_FILE, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for username, password in users.items():
            writer.writerow({'username': username, 'password': password})

def create_backup():
    if os.path.exists(DB_FILE):
        shutil.copy(DB_FILE, f"{DB_FILE}.bak")