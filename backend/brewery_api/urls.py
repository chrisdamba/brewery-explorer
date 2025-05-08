from django.urls import path
from .views import BreweryListView, BreweryDetailView, BrewerySearchView, RandomBreweryView

urlpatterns = [
    path('breweries/', BreweryListView.as_view(), name='brewery-list'),
    path('breweries/<str:brewery_id>/', BreweryDetailView.as_view(), name='brewery-detail'),
    path('breweries/search/', BrewerySearchView.as_view(), name='brewery-search'),
    path('breweries/random/', RandomBreweryView.as_view(), name='random-brewery'),
]
