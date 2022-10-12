import requests
from rest_framework import viewsets

from .models import Pokemon
from .serializer import PokemonSerializer


class pokemonViewset(viewsets.ModelViewSet):
    """This Class/ViewSet represents the Core functionality of Pokemon 
    Display/Discovery Feature. 
    
    If a requested Pokemon is missing in the MiddleWare we try to update it
    through by making a request to the Pokemon API and update the
    same in the MiddleWare.

    Desc:
        Method Supported : GET

        URL Supported:
        /crawler/
        /crawler/?name=xxxx

    Returns: JSON Response
    """
    # TODO: Need to add Pagination with a page size of 20. 
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    http_method_names = ['get']

    def extract_required_data(self, data):
        """This method represents required data extraction from Pokemon 3rd
        Party API request.

        Currently Considering the first/base value in the Pokemon API Response.
        """        
        name = data['name']
        stats = data['stats'][0]['base_stat']
        abilities = data['abilities'][0]['ability']['name']
        Moves = data['moves'][0]['move']['name']
        weight = data['weight']
        description = f"{name} {stats} {abilities} {weight}"
        return {
                "name": name,
                "stats": stats,
                "abilities": abilities,
                "Moves": Moves,
                "weight": weight,
                "description": description,
        }

    def insert_missing_data(self, required_data):
        """This method inserts data into DB."""
        #TODO: Surround it by try:except block.
        Pokemon.objects.create(
            name=required_data.get('name'),
            stats=required_data.get('stats'),
            abilities=required_data.get('abilities'),
            Moves=required_data.get('Moves'),
            weight=required_data.get('weight'),
            description=required_data.get('description')
        )

    def get_missing_pokemon(self, name):
        # TODO: Add all the constants into Constant file.
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{name}"
            response = requests.get(url=url)
            data = response.json()
            return self.extract_required_data(data)
        except requests.exceptions.RequestException as err:
            return {}

    def get_queryset(self):
        """This method is overidding the get_queryset method to get the query
        string in GET API.
        Currently supporting filtering by `name` attribute.
        """
        name = self.request.GET.get('name', None)
        if name:
            if Pokemon.objects.filter(name__icontains=name).exists():
                self.queryset = Pokemon.objects.filter(name__icontains=name)
            else:
                # make a request
                required_data = self.get_missing_pokemon(name)
                if required_data:
                    self.insert_missing_data(required_data)
                    self.queryset = Pokemon.objects.filter(name__icontains=name)
        return self.queryset
