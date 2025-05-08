from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.brewery_service import BreweryService


class BreweryListView(APIView):
    """API endpoint to fetch and filter breweries"""

    def get(self, request):
        params = {}
        for key, value in request.query_params.items():
            if value and key not in ['group_by']:
                params[key] = value

        try:
            breweries = BreweryService.get_breweries(params)

            group_by = request.query_params.get('group_by')
            if group_by and breweries:
                grouped_data = BreweryService.group_breweries_by_attribute(breweries, group_by)

                group_counts = {k: len(v) for k, v in grouped_data.items()}

                return Response({
                    'grouped': grouped_data,
                    'group_counts': group_counts,
                    'breweries': breweries
                })

            return Response(breweries)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BreweryDetailView(APIView):
    """API endpoint to fetch a specific brewery by ID"""

    def get(self, request, brewery_id):
        try:
            brewery = BreweryService.get_brewery_by_id(brewery_id)
            if not brewery:
                return Response(
                    {'error': 'Brewery not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(brewery)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BrewerySearchView(APIView):
    """API endpoint to search breweries by keyword"""

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response(
                {'error': 'Search query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            breweries = BreweryService.search_breweries(query)
            return Response(breweries)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RandomBreweryView(APIView):
    """API endpoint to get a random brewery"""

    def get(self, request):
        try:
            brewery = BreweryService.get_random_brewery()
            return Response(brewery)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
