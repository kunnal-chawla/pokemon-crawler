import json

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Pokemon


class PokemonTestCase(TestCase):

    expected_result_qs = [
        {'name': 'ditto', 
        'description': 'ditto 48 limber 40', 
        'stats': '45', 
        'abilities': 'overgrow', 
        'Moves': 'razor-wind', 
        'weight': '69'}
        ]

    expected_result_all = [
        {'name': 'bulbasaur', 
        'description': 'bulbasaur 45 overgrow 69', 
        'stats': '45', 
        'abilities': 'overgrow', 
        'Moves': 'razor-wind', 'weight': '69'}, 
        {'name': 'ditto', 
        'description': 'ditto 48 limber 40', 
        'stats': '45', 
        'abilities': 'overgrow', 
        'Moves': 'razor-wind', 
        'weight': '69'}
        ]
    
    expected_missing_result = [
        {'name': 'venusaur', 
        'description': 'venusaur 80 overgrow 1000', 
        'stats': '80', 
        'abilities': 'overgrow', 
        'Moves': 'swords-dance', 
        'weight': '1000'}
        ]

    def setUp(self):
        self.client = APIClient()
        Pokemon.objects.create(
            name="bulbasaur",
            stats="45",
            abilities="overgrow",
            Moves="razor-wind",
            weight="69",
            description="bulbasaur 45 overgrow 69"
        )
        Pokemon.objects.create(
            name="ditto",
            stats="45",
            abilities="overgrow",
            Moves="razor-wind",
            weight="69",
            description="ditto 48 limber 40"
        )

    def test_get_all_pokemon(self):
        """Pokemon that are in DB is been displayed."""
        response = self.client.get(f"/crawler/")
        result = json.loads(response.content.decode('utf-8'))
        assert self.expected_result_all == result

    def test_get_pokemon_by_query_string(self):
        """Pokemon been filtered based on name ditto."""
        name = "ditto"
        response = self.client.get(f"/crawler/?name={name}")
        result = json.loads(response.content.decode('utf-8'))
        assert self.expected_result_qs == result

    def test_get_missing_pokemon_by_query_string(self):
        """Pokemon been filtered based on name venusaur."""
        name = "venusaur"
        response = self.client.get(f"/crawler/?name={name}")
        result = json.loads(response.content.decode('utf-8'))
        assert self.expected_missing_result == result
