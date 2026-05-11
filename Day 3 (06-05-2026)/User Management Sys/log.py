import datetime

LOG_FILE = "activity.log"

def log_activity(username, action):
    """Bonus: Logs user activity with a detailed timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User: {username} | Action: {action}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)