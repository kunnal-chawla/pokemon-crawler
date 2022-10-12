from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import pokemonViewset

# Created a router and register our Pokemon viewsets with it.
router = DefaultRouter()
router.register(r'', pokemonViewset, basename="display-pokemon")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
