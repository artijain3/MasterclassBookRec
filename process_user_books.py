from playwright.sync_api import sync_playwright
from db import get_user
from user import User, LoginType

def handle_response(response):
    if response.status == 400:
        print("400 ERROR DETECTED: {response.url}") #TODO: make more robust for specific errors later
    
def web_browser_log_in(account):
    """
    This function uses playwright to log in and access a private user account.
    
    Inputs:
        user_email
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.on("response", handle_response)
        
        page.goto("https://www.goodreads.com/user/sign_in")
        page.get_by_text("Sign in with email").click()
        page.wait_for_load_state("load")
        
        # get account: user_email
        # account = pickle.get(user_email)
        login_type = account.login_type
        
        if login_type == LoginType.EMAIL:
            # call login
            email, pw = account.login()
            page.fill("#ap_email", email)
            page.fill("#ap_password", pw)
            page.get_by_text("Sign in").click()
            page.wait_for_load_state("load")
        # elif login_type == LogingType.AMAZON
        # elif login_type == LogingType.APPLE
        # elif login_type == LogingType.GOOGLE
        # elif login_type == LogingType.NEW
        
        # After the page is loaded
        # hmm what to do if captcha is there?
        page.get_by_text("My Books").click()
        page.wait_for_load_state("load")
        current_url = page.url
        
        
        https://www.goodreads.com/review/list/4615184?ref=nav_mybooks
        
        https://www.goodreads.com/review/list/4615184-arti?ref=nav_mybooks&shelf=read

def get_user_books(user_email):
    """
    There are multiple ways to get a user's book data:
    1. Public Profile --> go to users's "read-books" shelf
    2. Download CSV of book data if user is logged in
    3. User can provide the CSV data of their Goodreads Shelf
    4. If the profile or read-books is private, then the user needs to log in and allow permission (playwright)
    """
    account = get_user(user_email)
    if not account:
        #TODO: later ask User to enter in details to make new account
        raise ValueError(f"No account found with user email: {user_email}.")
    
    web_browser_log_in(account)
