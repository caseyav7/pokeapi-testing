def test_get_pokemon_list_default(poke_client):
    resp = poke_client.get_pokemon_list()
    assert resp.status_code == 200

    data = resp.json()
    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) > 0


def test_list_pokemon_structure(poke_client):
    """
    Ensure each entry in results has name + url.
    """
    resp = poke_client.get_pokemon_list(limit=10)
    assert resp.status_code == 200

    results = resp.json()["results"]
    for entry in results:
        assert "name" in entry
        assert "url" in entry


import pytest

@pytest.mark.parametrize("limit,offset", [
    (5, 0),
    (10, 20),
    (15, 30),
])
def test_pokemon_list_pagination(poke_client, limit, offset):
    resp = poke_client.get_pokemon_list(limit=limit, offset=offset)
    assert resp.status_code == 200

    results = resp.json()["results"]
    assert len(results) <= limit