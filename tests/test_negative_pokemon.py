def test_nonexistent_pokemon_returns_404(poke_client):
    resp = poke_client.get_pokemon("definitely-not-real-99999")
    assert resp.status_code == 404


def test_invalid_endpoint_returns_404(poke_client):
    resp = poke_client.get("not-a-valid-endpoint")
    assert resp.status_code == 404


def test_pokemon_list_invalid_limit(poke_client):
    resp = poke_client.get("pokemon", limit="abc", offset=0)
    # PokeAPI ignores invalid params and returns 200 with default pagination
    assert resp.status_code == 200