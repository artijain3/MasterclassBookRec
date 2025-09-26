import pickle
from playwright.sync_api import sync_playwright
from enum import Enum
import os


PICKLE_FILE = "users.pkl"

class LoginType(Enum):
    EMAIL = "email"
    AMAZON = "amazon"
    APPLE = "apple"
    GOOGLE = "google"
    NEW_ACCOUNT = "new"


# This is the User class where a user's email and password are stored. This will get stored in a pickle file.
class User:
    def __init__(self, login_type: LoginType, email: str):
        if not isinstance(login_type, LoginType):
            raise ValueError(f"Invalid login_type: {login_type}. Must be one of {[lt.value for lt in LoginType]}")
        if login_type == LoginType.NEW:
            return "You must have an existing Goodreads account. Please create one by visiting https://www.goodreads.com/user/sign_up"
        
        self.email = email
        self.login_type = login_type
        self._password = None
        self._validated_password = False
        
    def _get_password(self):
        password = input("Please enter your Goodreads password.")
        self._password = password
        
        # validate password
        if self.login_type == LoginType.EMAIL:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True) 
                page = browser.new_page()
                
                def handle_response(response):
                    if response.status == 400:
                        print("400 ERROR DETECTED: {response.url}") #TODO: make more robust for specific errors later
                        self._login_failed = True
                    
                page.on("response", handle_response)
                page.goto("https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D")
                page.fill("#ap_email", self.email)
                page.fill("#ap_password", self._password)
                page.wait_for_load_state("load")
                page.get_by_text("Sign in").click()
                browser.close()    
        
        if not self._login_failed:
            self._validated_password = True
        else:
            self._validated_password = False

    def login(self):
        if not self._password or not self._validated_password:
            self._get_password()
        return self.email, self._password
    
    
# Database Functions
def load_all_users():
    if not os.path.exists(PICKLE_FILE):
        return {}
    with open(PICKLE_FILE, "rb") as f:
        return pickle.load(f)

def save_all_users(users):
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(users, f)