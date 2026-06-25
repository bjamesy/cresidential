from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SANDBOX_SECRET_KEY = os.getenv("PLAID_SANDBOX_SECRET_KEY")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")
