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
    assert 'Jane Doe and John Roe</a></li>' in response.text
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
    assert 'Ben Smith <br>' in response.text
    assert 'Becky Smith <br>' in response.text
