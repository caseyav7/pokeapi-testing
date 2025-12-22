import pytest

@pytest.mark.smoke
@pytest.mark.regression
def test_get_pokemon_list_default(poke_client):
    resp = poke_client.get_pokemon_list()
    assert resp.status_code == 200

    data = resp.json()
    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) > 0

@pytest.mark.regression
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

@pytest.mark.regression
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

@pytest.mark.regression
def test_first_list_entry_matches_details(poke_client):
    resp_list = poke_client.get_pokemon_list(limit=5, offset=0)
    assert resp_list.status_code == 200

    data = resp_list.json()
    first_entry = data["results"][0]

    # The first entry should have a name and a url
    list_name  = first_entry["name"]
    list_url = first_entry["url"]
    assert list_name, list_url

    # Call the detail endpoint using the API client by name
    resp_detail = poke_client.get_pokemon(list_name)
    assert resp_detail.status_code == 200

    detail_data = resp_detail.json()
    # The name from the detail endpoint should match the list entry
    assert detail_data["name"] == list_name

@pytest.mark.regression
@pytest.mark.data_quality
def test_pokemon_names_are_lowercase_in_list(poke_client):
    resp = poke_client.get_pokemon_list(limit=20, offset=0)
    assert resp.status_code == 200

    results = resp.json()["results"]
    for entry in results:
        name = entry["name"]
        assert name == name.lower(), f"Expected lowercase name, got '{name}"

@pytest.mark.regression
def test_pokemon_pagination_do_not_overlap(poke_client):
    resp_page1 = poke_client.get_pokemon_list(limit=10, offset=0)
    resp_page2 = poke_client.get_pokemon_list(limit=10, offset=10)
    assert resp_page1.status_code == 200
    assert resp_page2.status_code == 200

    data1 = resp_page1.json()["results"]
    data2 = resp_page2.json()["results"]

    names_page1 = {p["name"] for p in data1}
    names_page2 = {p["name"] for p in data2}

    assert len(names_page1) > 0
    assert len(names_page2) > 0

    overlap = names_page1 & names_page2
    assert not overlap, f"Expected no overlap between pages, but found: {overlap}"