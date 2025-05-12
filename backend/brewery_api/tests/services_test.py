import unittest
from unittest.mock import patch, MagicMock
from brewery_api.services.brewery_service import BreweryService
import requests.exceptions


class BreweryServiceTests(unittest.TestCase):
    @patch('brewery_api.services.brewery_service.requests.get')
    def test_get_breweries_success(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": "1", "name": "Test Brewery"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call service
        result = BreweryService.get_breweries({"by_type": "micro"})

        # Assertions
        mock_get.assert_called_once_with("https://api.openbrewerydb.org/v1/breweries", params={"by_type": "micro"})
        self.assertEqual(result, [{"id": "1", "name": "Test Brewery"}])

    @patch('brewery_api.services.brewery_service.requests.get')
    def test_get_breweries_error(self, mock_get):
        # Mock error response
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # Call service
        result = BreweryService.get_breweries()

        # Assert empty list returned on error
        self.assertEqual(result, [])

    @patch('brewery_api.services.brewery_service.requests.get')
    def test_get_brewery_by_id_success(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "name": "Test Brewery"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call service
        result = BreweryService.get_brewery_by_id("123")

        # Assertions
        mock_get.assert_called_once_with("https://api.openbrewerydb.org/v1/breweries/123")
        self.assertEqual(result, {"id": "123", "name": "Test Brewery"})

    def test_group_breweries_by_attribute(self):
        # Test data
        breweries = [
            {"id": "1", "brewery_type": "micro", "name": "Brewery A"},
            {"id": "2", "brewery_type": "brewpub", "name": "Brewery B"},
            {"id": "3", "brewery_type": "micro", "name": "Brewery C"}
        ]

        # Call service
        result = BreweryService.group_breweries_by_attribute(breweries, "brewery_type")

        # Assertions
        self.assertEqual(len(result), 2)  # Two groups
        self.assertEqual(len(result["micro"]), 2)  # 2 micro breweries
        self.assertEqual(len(result["brewpub"]), 1)  # 1 brewpub
        self.assertEqual(result["micro"][0]["name"], "Brewery A")
        self.assertEqual(result["micro"][1]["name"], "Brewery C")