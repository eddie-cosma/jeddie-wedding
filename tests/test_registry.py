import pytest

from . import app, client, runner


def test_load_registry(client):
    response = client.get('/en/registry')
    assert '<h1>Gift registry</h1>' in response.text


def test_custom_registry_item_get(client):
    response = client.get('/en/registry/custom')
    assert 'Enter a custom gift amount below.' in response.text


@pytest.mark.parametrize('price', ['0', '-1', 'abc', '0.05', '5001', '0.12345'])
def test_custom_registry_item_post_invalid_price(client, price):
    payload = {
        'price': price,
    }
    response = client.post('/en/registry/custom', data=payload)
    assert 'You must enter a dollar amount between $1 and $5000' in response.text


@pytest.mark.parametrize('price', ['1', '50', '50.50', '5000', '4.5678'])
def test_custom_registry_item_post_valid_price(client, price):
    payload = {
        'price': price,
    }
    response = client.post('/en/registry/custom', data=payload)
    assert response.status_code == 302
