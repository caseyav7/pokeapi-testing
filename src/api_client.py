import requests


class PokeApiClient:
    """
    Simple client wrapper for PokeAPI.
    """

    def __init__(self, base_url: str = "https://pokeapi.co/api/v2"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get(self, path: str, **params):
        """
        Generic GET request.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.get(url, params=params)

    def get_pokemon(self, name_or_id: str):
        """
        GET /pokemon/{id or name}
        """
        return self.get(f"pokemon/{name_or_id}")

    def get_pokemon_list(self, limit: int = 20, offset: int = 0):
        """
        GET /pokemon?limit=&offset=
        """
        return self.get("pokemon", limit=limit, offset=offset)