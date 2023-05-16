import pytest

from . import app, client, runner


def test_rsvp_no_name_post(client):
    payload = {
        'g-recaptcha-response': 'test'
    }
    response = client.post('/en/rsvp_search', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_search', data=payload, follow_redirects=True)
    assert '<label for="name">Name</label> <input type="text" name="name" id="name" value="" required>' in response.text
    assert '<div class="g-recaptcha" data-sitekey="' in response.text


def test_rsvp_no_results_post(client):
    payload = {
        'g-recaptcha-response': 'test',
        'name': 'NoResultSearch'
    }
    response = client.post('/en/rsvp_search', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_search', data=payload, follow_redirects=True)
    assert 'We could not find your name on the guest list' in response.text
    assert '<label for="name">Name</label> <input type="text" name="name" id="name" value="" required>' in response.text
    assert '<div class="g-recaptcha" data-sitekey="' in response.text


@pytest.mark.parametrize('name', ['Doe', 'doe'])
def test_rsvp_multiple_results_post(client, name):
    payload = {
        'g-recaptcha-response': 'test',
        'name': name
    }
    response = client.post('/en/rsvp_search', data=payload)
    assert response.status_code == 200
    assert 'John Doe</a></li>' in response.text
    assert 'James Doe</a></li>' in response.text


@pytest.mark.parametrize('name', ['Smith', 'smith'])
def test_rsvp_multiple_results_same_party_post(client, name):
    payload = {
        'g-recaptcha-response': 'test',
        'name': name
    }
    response = client.post('/en/rsvp_search', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_search', data=payload, follow_redirects=True)
    assert '<input type="text" name="first_name" id="first_name" value="Ben" required>' in response.text
    assert '<input type="text" name="last_name" id="last_name" value="Smith" required>' in response.text
    assert '<input type="text" name="first_name" id="first_name" value="Becky" required>' in response.text
