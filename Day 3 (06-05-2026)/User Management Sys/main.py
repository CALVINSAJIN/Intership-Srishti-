import sys
from auth import register_user, authenticate_user
from file_handler import load_users, save_users
from utils import encrypt_data, validate_password
from exceptions import UserManagementError, UserAlreadyExistsError, AuthenticationError
from log import log_activity

def dashboard(username):
    """User Dashboard for viewing, updating, and deleting accounts."""
    while True:
        print(f"\n--- Dashboard: Welcome {username} ---")
        print("1. View Profile")
        print("2. Update Password")
        print("3. Delete Account")
        print("4. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            print(f"\n[Profile] Username: {username}")
        
        elif choice == '2':
            new_pwd = input("Enter new password: ")
            is_valid, msg = validate_password(new_pwd)
            if is_valid:
                users = load_users()
                users[username] = encrypt_data(new_pwd)
                save_users(users)
                log_activity(username, "Password Updated")
                print("Password updated successfully.")
            else:
                print(f"Update Failed: {msg}")
        
        elif choice == '3':
            confirm = input("Are you sure you want to delete your account? (y/n): ")
            if confirm.lower() == 'y':
                users = load_users()
                if username in users:
                    del users[username]
                    save_users(users)
                    log_activity(username, "Account Deleted")
                    print("Account deleted. Logging out...")
                    break
        
        elif choice == '4':
            log_activity(username, "Logout")
            print("Logged out successfully.")
            break
        else:
            print("Invalid selection. Try again.")

def main():
    """Main entry point for the User Management System."""
    while True:
        print("\n=== Smart User Management System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choice: ")

        if choice == '1':
            u = input("Enter Username: ")
            p = input("Enter Password: ")
            try:
                register_user(u, p)
                print("Registration successful!")
            except (UserAlreadyExistsError, ValueError) as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                # Requirement: Use try-except-finally block
                print("Registration request processed.")

        elif choice == '2':
            attempts = 0
            # Requirement: Login system with 3 attempts
            while attempts < 3:
                u = input("Username: ")
                p = input("Password: ")
                try:
                    if authenticate_user(u, p):
                        dashboard(u)
                        break
                except AuthenticationError as e:
                    attempts += 1
                    print(f"{e} Attempts left: {3 - attempts}")
                except Exception as e:
                    print(f"Error: {e}")
                    break
            else:
                print("Maximum login attempts reached. Returning to main menu.")

        elif choice == '3':
            print("Exiting system. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()