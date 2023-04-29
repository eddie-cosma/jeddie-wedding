import pytest

from . import app, client, runner


# def test_rsvp_no_code(client):
#     response = client.get('/en/rsvp')
#     assert '<label for="rsvp_code">RSVP code:</label> <input id="rsvp_code" type="text"><br>' in response.text
#     assert '<input id="rsvp_code" type="hidden"' not in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' in response.text
#
#
# def test_rsvp_with_code(client):
#     response = client.get('/en/rsvp/12345A')
#     assert '<input id="rsvp_code" type="hidden" value="12345A"><br>' in response.text
#     assert '<label for="rsvp_code">RSVP code:</label> <input id="rsvp_code" type="text"><br>' not in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' in response.text
#
#
# def test_rsvp_no_code_post(client):
#     payload = {
#         'g-recaptcha-response': 'test',
#     }
#     response = client.post('/en/rsvp', data=payload)
#     assert response.status_code == 302
#
#     response = client.post('/en/rsvp', data=payload, follow_redirects=True)
#     assert '<label for="rsvp_code">RSVP code:</label> <input id="rsvp_code" type="text"><br>' in response.text
#     assert '<input id="rsvp_code" type="hidden"' not in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' in response.text
#
#
# def test_rsvp_with_incorrect_code_post(client):
#     payload = {
#         'g-recaptcha-response': 'test',
#         'rsvp_code': 'ABCDEF'
#     }
#     response = client.post('/en/rsvp', data=payload)
#     assert response.status_code == 302
#
#     response = client.post('/en/rsvp', data=payload, follow_redirects=True)
#     assert '<label for="rsvp_code">RSVP code:</label> <input id="rsvp_code" type="text"><br>' in response.text
#     assert '<input id="rsvp_code" type="hidden"' not in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' in response.text
#
#
# def test_rsvp_with_incorrect_code_url_post(client):
#     payload = {
#         'g-recaptcha-response': 'test',
#     }
#     response = client.post('/en/rsvp/ABCDEF', data=payload)
#     assert response.status_code == 302
#
#     response = client.post('/en/rsvp/ABCDEF', data=payload, follow_redirects=True)
#     assert '<label for="rsvp_code">RSVP code:</label> <input id="rsvp_code" type="text"><br>' in response.text
#     assert '<input id="rsvp_code" type="hidden"' not in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' in response.text
#
#
# def test_rsvp_with_code_post(client):
#     payload = {
#         'g-recaptcha-response': 'test',
#         'rsvp_code': '12345A'
#     }
#     response = client.post('/en/rsvp', data=payload)
#     assert 'Welcome, John and Jane' in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' not in response.text
#
#
# def test_rsvp_with_code_url_post(client):
#     payload = {
#         'g-recaptcha-response': 'test',
#     }
#     response = client.post('/en/rsvp/12345A', data=payload)
#     assert 'Welcome, John and Jane' in response.text
#     assert '<div class="g-recaptcha" data-sitekey="' not in response.text
#
#
# def test_rsvp_with_plus_one(client):
#     payload = {
#         'g-recaptcha-response': 'test',
#     }
#     response = client.post('/en/rsvp/12345B', data=payload)
#     assert 'Welcome, Ben and Becky' in response.text
#     assert '<input type="button" id="add_guests_button"' in response.text