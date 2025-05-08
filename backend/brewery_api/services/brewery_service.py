import requests
from typing import Dict, List, Any, Optional


class BreweryService:
    """Service to interact with Open Brewery DB API"""

    BASE_URL = "https://api.openbrewerydb.org/breweries"

    @classmethod
    def get_breweries(cls, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Fetch breweries from the Open Brewery DB API with optional filters

        Args:
            params: Optional dictionary of query parameters for filtering

        Returns:
            List of brewery dictionaries
        """
        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log error in production
            print(f"Error fetching breweries: {e}")
            return []

    @classmethod
    def get_brewery_by_id(cls, brewery_id: str) -> Dict[str, Any]:
        """
        Fetch a specific brewery by ID

        Args:
            brewery_id: Brewery ID to fetch

        Returns:
            Dictionary with brewery details
        """
        try:
            response = requests.get(f"{cls.BASE_URL}/{brewery_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log error in production
            print(f"Error fetching brewery {brewery_id}: {e}")
            return {}

    @classmethod
    def search_breweries(cls, query: str) -> List[Dict[str, Any]]:
        """
        Search breweries by keyword

        Args:
            query: Search term

        Returns:
            List of matching brewery dictionaries
        """
        try:
            response = requests.get(f"{cls.BASE_URL}/search", params={"query": query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching breweries: {e}")
            return []

    @classmethod
    def get_random_brewery(cls) -> Dict[str, Any]:
        """
        Get a random brewery

        Returns:
            Dictionary with random brewery details
        """
        try:
            response = requests.get(f"{cls.BASE_URL}/random")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching random brewery: {e}")
            return {}

    @classmethod
    def group_breweries_by_attribute(cls, breweries: List[Dict], attribute: str) -> Dict[str, List]:
        """
        Group breweries by a given attribute

        Args:
            breweries: List of brewery dictionaries
            attribute: Attribute to group by

        Returns:
            Dictionary with groups as keys and lists of breweries as values
        """
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
