from datetime import date, timedelta
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from app.config import PLAID_CLIENT_ID, PLAID_SANDBOX_SECRET_KEY, PLAID_ENV


def get_plaid_client():
    env_map = {
        "sandbox": plaid.Environment.Sandbox,
        "development": plaid.Environment.Development,
        "production": plaid.Environment.Production,
    }
    configuration = plaid.Configuration(
        host=env_map.get(PLAID_ENV, plaid.Environment.Sandbox),
        api_key={"clientId": PLAID_CLIENT_ID, "secret": PLAID_SANDBOX_SECRET_KEY},
    )
    return plaid_api.PlaidApi(plaid.ApiClient(configuration))


def fetch_transactions(access_token: str) -> list[dict]:
    client = get_plaid_client()
    end_date = date.today()
    start_date = end_date - timedelta(days=365 * 2)

    all_transactions = []
    offset = 0

    while True:
        response = client.transactions_get(
            TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
                options=TransactionsGetRequestOptions(offset=offset, count=500),
            )
        )
        transactions = response.transactions
        all_transactions.extend(transactions)
        offset += len(transactions)
        if offset >= response.total_transactions:
            break

    return [
        {
            "date": str(t.date),
            "amount": t.amount,
            "description": t.merchant_name or t.name or "",
        }
        for t in all_transactions
        if t.amount > 0  # outflows in Plaid are positive amounts
    ]
