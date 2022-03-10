def test_ma01_homepage_valid(test_client):
    response = test_client.get('/')
    assert b'Ripa' in response.data

def test_ma02_homepage_valid(test_client):
    response = test_client.get('/')
    assert b'Danielle' not in response.data