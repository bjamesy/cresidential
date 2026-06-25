import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from app.config import PLAID_CLIENT_ID, PLAID_SANDBOX_SECRET_KEY, PLAID_ENV
from app import store

router = APIRouter()


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


class ExchangeTokenRequest(BaseModel):
    public_token: str


@router.post("/create-link-token")
def create_link_token():
    client = get_plaid_client()
    try:
        response = client.link_token_create(
            LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(client_user_id="mvp-user"),
                client_name="Rental Verification",
                products=[Products("transactions")],
                country_codes=[CountryCode("US")],
                language="en",
            )
        )
        return {"link_token": response.link_token}
    except plaid.ApiException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/exchange-token")
def exchange_token(body: ExchangeTokenRequest):
    client = get_plaid_client()
    try:
        response = client.item_public_token_exchange(
            ItemPublicTokenExchangeRequest(public_token=body.public_token)
        )
        session_id = str(uuid.uuid4())
        store.sessions[session_id] = response.access_token
        return {"session_id": session_id}
    except plaid.ApiException as e:
        raise HTTPException(status_code=400, detail=str(e))
