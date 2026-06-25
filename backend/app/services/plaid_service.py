from datetime import date, timedelta
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from app.config import PLAID_CLIENT_ID, PLAID_SANDBOX_SECRET_KEY, PLAID_ENV

TWO_YEARS_AGO = date.today() - timedelta(days=365 * 2)


def get_plaid_client():
    env_map = {
        "sandbox": plaid.Environment.Sandbox,
        "production": plaid.Environment.Production,
    }
    configuration = plaid.Configuration(
        host=env_map.get(PLAID_ENV, plaid.Environment.Sandbox),
        api_key={"clientId": PLAID_CLIENT_ID, "secret": PLAID_SANDBOX_SECRET_KEY},
    )
    return plaid_api.PlaidApi(plaid.ApiClient(configuration))


def fetch_transactions(access_token: str) -> list[dict]:
    client = get_plaid_client()
    all_transactions = []
    cursor = None

    while True:
        kwargs = {"access_token": access_token}
        if cursor:
            kwargs["cursor"] = cursor

        response = client.transactions_sync(TransactionsSyncRequest(**kwargs))
        all_transactions.extend(response.added)
        cursor = response.next_cursor

        if not response.has_more:
            break

    cutoff = TWO_YEARS_AGO
    return [
        {
            "date": str(t.date),
            "amount": t.amount,
            # name is more reliable than merchant_name in practice
            "description": t.name or t.merchant_name or "",
        }
        for t in all_transactions
        if t.amount > 0 and t.date >= cutoff  # outflows only, within 24 months
    ]
