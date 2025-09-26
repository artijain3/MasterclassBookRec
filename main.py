from db import all_users, add_or_update_user
from user import User, LoginType
from process_user_books import get_user_books

if __name__ == "__main__":
    # Example: add a new user
    u = User(LoginType.EMAIL, "test@example.com")
    add_or_update_user(u)

    # List all users
    print(all_users())

    # Try logging in
    get_user_books("test@example.com")