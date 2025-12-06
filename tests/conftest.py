import pytest
from src.api_client import PokeApiClient


@pytest.fixture(scope="session")
def poke_client():
    """
    Global fixture that returns a PokeAPI client instance.
    """
    return PokeApiClient()