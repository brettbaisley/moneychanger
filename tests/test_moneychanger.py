import pytest
import requests
from unittest.mock import patch, Mock
from moneychanger import get_exchange_rate

def test_get_exchange_rate_success():
    # Mock the successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "conversion_result": 123.456
    }
    
    with patch('requests.get', return_value=mock_response):
        # There appears to be a bug in the original function (missing return statement)
        # Testing the expected behavior if the function worked correctly
        result = get_exchange_rate("USD", "EUR", "100")
        
        # The function should return a tuple with formatted conversion result
        # This test will fail until the bug is fixed
        assert result == ("USD", "EUR", "100", "123.46")

def test_get_exchange_rate_http_error():
    # Mock a failed HTTP request
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    
    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate("USD", "EUR", "100")
        
        # Should return the input values with None for the conversion result
        assert result == ("USD", "EUR", "100", None)

def test_get_exchange_rate_connection_error():
    # Mock a connection error
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection refused")):
        result = get_exchange_rate("USD", "EUR", "100")
        
        # Should return the input values with None for the conversion result
        assert result == ("USD", "EUR", "100", None)

def test_get_exchange_rate_bad_status_code():
    # Mock a response with non-200 status code
    mock_response = Mock()
    mock_response.status_code = 403
    
    with patch('requests.get', return_value=mock_response):
        result = get_exchange_rate("USD", "EUR", "100")
        
        # Should return the input values with None for the conversion result
        assert result == ("USD", "EUR", "100", None)

