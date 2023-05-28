import pytest

from database.model import Party
from . import app, client, runner


def test_rsvp_no_name_post(client):
    payload = {
        'g-recaptcha-response': 'test'
    }
    response = client.post('/en/rsvp_search', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_search', data=payload, follow_redirects=True)
    assert '<label for="name">Last name</label> <input type="text" name="name" id="name" value="" required>' in response.text
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
    assert '<label for="name">Last name</label> <input type="text" name="name" id="name" value="" required>' in response.text
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
    assert '<h2>Ben Smith</h2>' in response.text
    assert '<h2>Becky Smith</h2>' in response.text


def test_rsvp_invalid_party(client):
    response = client.get('/en/rsvp_detail/123456')
    assert response.status_code == 302

    response = client.get('/en/rsvp_detail/123456', follow_redirects=True)
    assert '<h1>RSVP Search</h1>' in response.text


def test_rsvp_empty_rsvp_response(client):
    response = client.post('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328', data={})
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328', data={}, follow_redirects=True)
    assert 'Thank you for your reservation.' in response.text


def test_rsvp_nobody_coming_response(client):
    payload = {
        '3': '0',
        '4': '0'
    }
    response = client.post('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328', data=payload, follow_redirects=True)
    assert 'Thank you for your reservation.' in response.text


def test_rsvp_someone_coming_response(client):
    payload = {
        '3': '1',
        '4': '0'
    }
    response = client.post('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328', data=payload, follow_redirects=True)
    assert '<h1>Ben Smith</h1>' in response.text
    assert '<h2>Meal choice</h2>' in response.text


def test_rsvp_invalid_party_on_guest_detail(client):
    response = client.get('/en/rsvp_detail/123456/1')
    assert response.status_code == 302

    response = client.get('/en/rsvp_detail/123456/1', follow_redirects=True)
    assert '<h1>RSVP Search</h1>' in response.text


def test_rsvp_invalid_guest_for_party(client):
    response = client.get('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328/0')
    assert response.status_code == 302

    response = client.get('/en/rsvp_detail/40820dfd-fd9d-4be7-872f-c57df7506328/0', follow_redirects=True)
    assert '<h1>RSVP Search</h1>' in response.text


def test_rsvp_missing_name_response(client):
    payload = {
        'meal': '2',
        'dietary_restrictions': '',
        'song_choice': ''
    }
    response = client.post('/en/rsvp_detail/e8ea4d4d-c6ae-4b23-95a3-e91cc511521f/6', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/e8ea4d4d-c6ae-4b23-95a3-e91cc511521f/6', data=payload, follow_redirects=True)
    assert '<h1>RSVP Search</h1>' in response.text
    assert 'Please enter your first and last name.' in response.text


def test_rsvp_missing_meal_response(client):
    payload = {
        'first_name': 'First',
        'last_name': 'Last',
        'meal': '',
        'dietary_restrictions': '',
        'song_choice': ''
    }
    response = client.post('/en/rsvp_detail/e8ea4d4d-c6ae-4b23-95a3-e91cc511521f/6', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/e8ea4d4d-c6ae-4b23-95a3-e91cc511521f/6', data=payload, follow_redirects=True)
    assert '<h1>RSVP Search</h1>' in response.text
    assert 'Please select a meal option.' in response.text


def test_rsvp_successful_rsvp_with_more_guests(client):
    payload = {
        'meal': '1',
        'dietary_restrictions': '',
        'song_choice': ''
    }
    response = client.post('/en/rsvp_detail/e8ea4d4d-c6ae-4b23-95a3-e91cc511521f/5', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/e8ea4d4d-c6ae-4b23-95a3-e91cc511521f/5', data=payload, follow_redirects=True)
    assert '<h1>Guest of James Doe</h1>' in response.text


def test_rsvp_successful_rsvp_with_no_more_guests(client):
    payload = {
        'first_name': 'First',
        'last_name': 'Last',
        'meal': '1',
        'dietary_restrictions': '',
        'song_choice': ''
    }
    response = client.post('/en/rsvp_detail/97a0b846-a798-41a2-80de-cf0d81a1f596/1', data=payload)
    assert response.status_code == 302

    response = client.post('/en/rsvp_detail/97a0b846-a798-41a2-80de-cf0d81a1f596/1', data=payload, follow_redirects=True)
    assert '<h1>RSVP Search</h1>' in response.text

