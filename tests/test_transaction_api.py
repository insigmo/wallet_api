import random
from http import HTTPStatus

import pytest
from requests import HTTPError


def test_transaction(http_client, fake_data):
    balance = 100
    wallet_name = fake_data.user_name()
    wallet_data = {
        "data": {
            "type": "wallet",
            "attributes": {
                "label": wallet_name,
                "balance": balance
            }
        }
    }
    response = http_client.post('/wallet/', json=wallet_data)
    wallet_id = response.json()['data']["id"]

    assert wallet_id, f'Wallet {wallet_name} was not found'
    amount = random.randint(0, 10)
    body = {
        "data": {
            "type": "transaction",
            "attributes": {
                "wallet_id": str(wallet_id),
                "amount": amount
            }
        }
    }
    response = http_client.post('/transaction/', json=body)
    assert response.status_code == HTTPStatus.CREATED

    response = http_client.get('/transaction/', json=body)
    assert response.status_code == HTTPStatus.OK

    for transaction in response.json()['data']:
        if transaction['attributes']['wallet_id'] == str(wallet_id):
            assert transaction['type'] == "transaction"
            assert int(transaction['attributes']['amount']) == amount

    response = http_client.get('/wallet/', json=wallet_data)

    flag = False
    # TODO fix search with pagination
    for wallet in response.json()['data']:
        attributes = wallet["attributes"]
        if attributes["label"] == wallet_name:
            assert attributes["balance"] == balance + amount
            flag = True

    if not flag:
        raise AssertionError(f'wallet {wallet_name} was not found')


@pytest.mark.parametrize("body", [
    # negative balance wallet
    {
        "data": {
            "type": "wallet",
            "attributes": {
                "label": "invalid",
                "balance": -100
            }
        }
    },

    # invalid data no balance wallet
    {
        "data": {
            "type": "wallet",
            "attributes": {
                "label": "invalid",
                "balance": -100
            }
        }
    },

    # invalid data no label wallet
    {
        "data": {
            "type": "wallet",
            "attributes": {
                "balance": -100
            }
        }
    },

    # invalid data type wallets, not wallet
    {
        "data": {
            "type": "wallets",
            "attributes": {
                "label": "invalid",
                "balance": -100
            }
        }
    },
])
def test_negative_wallet(http_client, body):
    with pytest.raises(HTTPError):
        http_client.post('/wallet/', json=body)
