"""
This file is used to test the different components linked to the main blueprint, to check whether they are working
together properly. Especially the tests focus on the functionality that the user will be using and the required
interactions. These are mainly two and are with the flask application routes and the database.
"""


def test_ma01_homepage_valid(test_client):
    response = test_client.get('/home')
    assert response.status_code == 200
    assert b'IFP' in response.data, 'Footer not displayed'


def test_ma02_homepage_content(test_client):
    response = test_client.get('/home')
    assert b'Log In!' not in response.data, 'Incorrect page is displayed'
    assert b'Choropleth Map' in response.data, 'Navbar not displayed'
