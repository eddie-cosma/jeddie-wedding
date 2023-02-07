import pytest

from . import app, client, runner


@pytest.mark.parametrize('endpoint',
                         ['/en/', '/en/story', '/en/wedding', '/en/rsvp',
                          '/en/photos', '/en/hotel', '/en/registry'])
def test_basic_page_load(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize('endpoint',
                         ['/ro/', '/ro/story', '/ro/wedding', '/ro/rsvp',
                          '/ro/photos', '/ro/hotel', '/ro/registry'])
def test_internationalization(client, endpoint):
    response = client.get(endpoint)
    assert 'Nunta' in response.text


def test_landing_page_to_english_redirect(client):
    response = client.get('/')
    assert response.status_code == 302

    response = client.get('/', follow_redirects=True)
    assert 'We&#39;re getting married!' in response.text
