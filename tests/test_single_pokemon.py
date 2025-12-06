import pytest

@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_get_pokemon_by_name(poke_client, pokemon_name):
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200

    data = resp.json()
    assert data["name"] == pokemon_name
    assert "id" in data
    assert "types" in data
    assert len(data["types"]) >= 1


@pytest.mark.parametrize("pokemon_id", [1, 4, 25])
def test_get_pokemon_by_id(poke_client, pokemon_id):
    resp = poke_client.get_pokemon(str(pokemon_id))
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == pokemon_id
    assert "name" in data
    assert isinstance(data["types"], list)