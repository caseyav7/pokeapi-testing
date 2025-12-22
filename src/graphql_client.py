import requests

class PokeGraphQLClient:
    def __init__(self, endpoint: str = "https://graphql.pokeapi.co/v1beta2"):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def query(self, query: str, variables: dict | None = None, operation_name: str | None = None):
        payload = {
            "query": query,
            "variables": variables,
            "operationName": operation_name,
        }
        return self.session.post(self.endpoint, json=payload)