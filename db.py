from user import load_all_users, save_all_users

# Load once at startup
users = load_all_users()

def get_user(email):
    return users.get(email)

def add_or_update_user(user):
    users[user.email] = user
    save_all_users(users)

def all_users():
    return users