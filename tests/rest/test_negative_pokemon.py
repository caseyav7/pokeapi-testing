import pytest

@pytest.mark.negative
@pytest.mark.regression
def test_nonexistent_pokemon_returns_404(poke_client):
    resp = poke_client.get_pokemon("definitely-not-real-99999")
    assert resp.status_code == 404

@pytest.mark.negative
@pytest.mark.regression
def test_invalid_endpoint_returns_404(poke_client):
    resp = poke_client.get("not-a-valid-endpoint")
    """
    Some APIs return 404 for unknown routes, others use 400 (bad request).
    For PokeAPI, an invalid resource under /api/v2 currently returns 400.
    """
    assert resp.status_code in (400, 404), (
        f"Expected 400 or 404 for invalid endpoint, got {resp.status_code}. Body: {resp.text}"
    )

@pytest.mark.negative
@pytest.mark.regression
def test_pokemon_list_invalid_limit(poke_client):
    resp = poke_client.get("pokemon", limit="abc", offset=0)
    # PokeAPI ignores invalid params and returns 200 with default pagination
    assert resp.status_code == 200

@pytest.mark.negative
@pytest.mark.regression
def test_very_large_pokemon_id_returns_404(poke_client):
    # This ID is way beyond the current known Pokemon range
    resp = poke_client.get_pokemon("999999")
    assert resp.status_code == 404

