import pytest

from . import app, client, runner


@pytest.mark.parametrize('endpoint',
                         ['/', '/story', '/wedding', '/rsvp',
                          '/photos', '/hotel', '/registry'])
def test_basic_page_load(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
