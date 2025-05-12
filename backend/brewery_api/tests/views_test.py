from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
import logging


class BreweryViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('brewery_api.services.brewery_service.BreweryService.get_breweries')
    def test_brewery_list_view(self, mock_get_breweries):
        # Mock service response
        mock_get_breweries.return_value = [
            {"id": "1", "name": "Test Brewery A"},
            {"id": "2", "name": "Test Brewery B"}
        ]

        # Call API
        response = self.client.get(reverse('brewery-list'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Test Brewery A")

    @patch('brewery_api.services.brewery_service.BreweryService.get_breweries')
    @patch('brewery_api.services.brewery_service.BreweryService.group_breweries_by_attribute')
    def test_brewery_list_with_grouping(self, mock_group, mock_get_breweries):
        # Mock service responses
        mock_get_breweries.return_value = [
            {"id": "1", "brewery_type": "micro", "name": "Brewery A"},
            {"id": "2", "brewery_type": "brewpub", "name": "Brewery B"}
        ]

        mock_group.return_value = {
            "micro": [{"id": "1", "brewery_type": "micro", "name": "Brewery A"}],
            "brewpub": [{"id": "2", "brewery_type": "brewpub", "name": "Brewery B"}]
        }

        # Call API with grouping
        response = self.client.get(reverse('brewery-list') + '?group_by=brewery_type')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('grouped', response.data)
        self.assertIn('breweries', response.data)
        self.assertEqual(len(response.data['grouped']), 2)  # 2 groups

    @patch('brewery_api.services.brewery_service.BreweryService.get_brewery_by_id')
    def test_brewery_detail_view(self, mock_get_brewery):
        # Mock service response
        mock_get_brewery.return_value = {"id": "123", "name": "Test Brewery"}

        # Call API
        response = self.client.get(reverse('brewery-detail', args=["123"]))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], "123")
        self.assertEqual(response.data["name"], "Test Brewery")
