import pytest
from unittest.mock import patch, Mock
import sys
sys.path.append('..')
import requests
from Get_challengers_euw2.Classes_2 import api_string_constructor

def test_api_string_constructor_with_successful_response():
    # Mocking the requests module to return a successful response, that its able to 
    # iterate over search items and actually return a list of data
    with patch('Get_challengers_euw2.Classes_2.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'response': 'data'}
        mock_get.return_value = mock_response

        search_items = ['item1', 'item2']
        api_endpoint = 'https://example.com/api/{specific}?api_key={API_KEY}'
        API_KEY = 'my_api_key'

        response_data_list = api_string_constructor(search_items, api_endpoint, API_KEY)

        assert len(response_data_list) == 2
        assert response_data_list == [{'response': 'data'}, {'response': 'data'}]

def test_api_string_constructor_with_unsuccessful_response():
    # Mocking the requests module to return an unsuccessful response and checking that script exits
    with patch('Get_challengers_euw2.Classes_2.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        search_items = ['item1', 'item2']
        api_endpoint = 'https://example.com/api/{specific}?api_key={API_KEY}'
        API_KEY = 'my_api_key'

        with pytest.raises(SystemExit) as pytest_e:
            api_string_constructor(search_items, api_endpoint, API_KEY)
            assert pytest_e.type == SystemExit
            assert pytest_e.value.code == 404

def test_api_string_constructor_with_request_exception():
    # Mocking the requests module to raise a RequestException and checking that script exits
    with patch('Get_challengers_euw2.Classes_2.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException()

        search_items = ['item1', 'item2']
        api_endpoint = 'https://example.com/api/{specific}?api_key={API_KEY}'
        API_KEY = 'my_api_key'

        with pytest.raises(SystemExit) as pytest_e:
            api_string_constructor(search_items, api_endpoint, API_KEY)
            assert pytest_e.type == SystemExit