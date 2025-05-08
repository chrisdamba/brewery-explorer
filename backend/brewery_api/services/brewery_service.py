import requests
from typing import Dict, List, Any, Optional


class BreweryService:
    """Service to interact with Open Brewery DB API v1"""

    BASE_URL = "https://api.openbrewerydb.org/v1/breweries"

    @classmethod
    def get_breweries(cls, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Fetch breweries with optional filters"""
        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching breweries: {e}")
            return []

    @classmethod
    def get_brewery_by_id(cls, brewery_id: str) -> Dict[str, Any]:
        """Fetch a specific brewery by ID"""
        try:
            response = requests.get(f"{cls.BASE_URL}/{brewery_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching brewery {brewery_id}: {e}")
            return {}

    @classmethod
    def search_breweries(cls, query: str) -> List[Dict[str, Any]]:
        """Search breweries by keyword"""
        try:
            response = requests.get(f"{cls.BASE_URL}/search", params={"query": query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching breweries: {e}")
            return []

    @classmethod
    def get_random_brewery(cls, size: int = 1) -> List[Dict[str, Any]]:
        """Get random breweries"""
        try:
            response = requests.get(f"{cls.BASE_URL}/random", params={"size": size})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching random brewery: {e}")
            return []

    @classmethod
    def get_autocomplete(cls, query: str) -> List[Dict[str, Any]]:
        """Get autocomplete suggestions for a query"""
        try:
            response = requests.get(f"{cls.BASE_URL}/autocomplete", params={"query": query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching autocomplete: {e}")
            return []

    @classmethod
    def get_metadata(cls, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get metadata about breweries with optional filters"""
        try:
            response = requests.get(f"{cls.BASE_URL}/meta", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching metadata: {e}")
            return {}

    @classmethod
    def group_breweries_by_attribute(cls, breweries: List[Dict], attribute: str) -> Dict[str, List]:
        """Group breweries by attribute"""
        grouped = {}
        for brewery in breweries:
            key = brewery.get(attribute, 'unknown')
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(brewery)

        # Sort groups by count descending
        return {k: v for k, v in sorted(
            grouped.items(),
            key=lambda item: len(item[1]),
            reverse=True
        )}
