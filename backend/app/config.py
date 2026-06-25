from dotenv import load_dotenv
import os

load_dotenv()  # picks up .env from cwd or any parent; docker-compose injects vars directly

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SANDBOX_SECRET_KEY = os.getenv("PLAID_SANDBOX_SECRET_KEY")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")
