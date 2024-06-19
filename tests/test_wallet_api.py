from http import HTTPStatus

import pytest
from requests import HTTPError


def test_wallet(http_client, fake_data):
    expected = {
        "data": {
            "type": "wallet",
            "attributes": {
                "label": fake_data.user_name(),
                "balance": 100
            }
        }
    }
    response = http_client.post('/wallet/', json=expected)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["data"]['attributes'] == expected["data"]['attributes']

    response = http_client.get('/wallet/')
    assert response.status_code == HTTPStatus.OK
    assert response.json()["data"][-1]['attributes'] == expected["data"]['attributes']


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
