import pytest

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_get_pokemon_by_name(poke_client, pokemon_name):
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200

    data = resp.json()
    assert data["name"] == pokemon_name
    assert "id" in data
    assert "types" in data
    assert len(data["types"]) >= 1


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("pokemon_id", [1, 4, 25])
def test_get_pokemon_by_id(poke_client, pokemon_id):
    resp = poke_client.get_pokemon(str(pokemon_id))
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == pokemon_id
    assert "name" in data
    assert isinstance(data["types"], list)

@pytest.mark.regression
@pytest.mark.domain
@pytest.mark.parametrize(
    "pokemon_name, expected_types",
    [
        ("pikachu", {"electric"}),
        ("bulbasaur", {"grass", "poison"}),
        ("charmander", {"fire"}),
    ],
)
def test_pokemon_has_expected_types(poke_client, pokemon_name, expected_types):
    """Ensure certain well-known Pokémon have the expected types."""
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200

    data = resp.json()
    type_names = {t["type"]["name"] for t in data["types"]}

    # Every expected type should be present in the pokemon's type list
    for expected in expected_types:
        assert expected in type_names, (
            f"{pokemon_name} is expected to have type '{expected}', "
            f"but types were {type_names}."
        )

@pytest.mark.regression
@pytest.mark.data_quality
@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_pokemon_base_stats_are_in_reasonable_range(poke_client, pokemon_name):
    """
    Verify that base stats for some well-known Pokemon sare within a realistic range.
    This helps catch weird data issues like 0 or insanely large numbers.
    """
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200

    data = resp.json()
    stats = data["stats"]

    # We expect that each Pokemon to have at least one stat defines.
    assert len(stats) > 0

    for stat_entry in stats:
        base = stat_entry["base_stat"]
        stat_name = stat_entry["stat"]["name"]

        assert isinstance(base, int), f"{pokemon_name} has non-int base_stat for {stat_name}: {base}"
        assert 1 <= base <= 255, (
            f"{pokemon_name} has unrealistic base_stat for {stat_name}: {base} "
            "(expected between 1 and 255)"
        )

@pytest.mark.regression
@pytest.mark.data_quality
@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_pokemon_height_weight_are_positive(poke_client, pokemon_name):
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200
    data = resp.json()
    height = data["height"]
    weight = data["weight"]
    assert isinstance(height, int), f"{pokemon_name} has non-int height: {height}"
    assert isinstance(weight, int), f"{pokemon_name} has non-int weight: {weight}"
    assert height > 0, f'{pokemon_name} has non-positive height: {height}'
    assert weight > 0, f'{pokemon_name} has non-positive weight: {weight}'

@pytest.mark.regression
@pytest.mark.data_quality
@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_pokemon_has_at_least_one_ability(poke_client, pokemon_name):
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200
    data = resp.json()
    abilities = data["abilities"]
    assert isinstance(abilities, list), f"{pokemon_name} has non-list abilities: {abilities}"
    assert len(abilities) > 0, f"{pokemon_name} has no abilities defined"

@pytest.mark.regression
@pytest.mark.data_quality
@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_pokemon_species_url_returns_200(poke_client, pokemon_name):
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200
    data = resp.json()

    species = data["species"]
    species_url = data["species"]["url"]
    assert isinstance(species, dict), f"{pokemon_name} has non-list species: {species}"
    assert len(species) > 0, f"{pokemon_name} has no species defined"
    assert isinstance(species_url, str), f"{pokemon_name} has non-str species url: {species_url}"
    assert len(species_url) > 0, f"{pokemon_name} has no species url defined"

    species_resp = poke_client.get_pokemon(pokemon_name)
    assert species_resp.status_code == 200, (
        f"Species URL for {pokemon_name} returned {species_resp.status_code},"
        f"body: {species_resp.text}"
    )
@pytest.mark.regression
@pytest.mark.data_quality
@pytest.mark.parametrize("pokemon_name", ["pikachu", "bulbasaur", "charmander"])
def test_pokemon_all_stat_names_are_valid(poke_client, pokemon_name):
    resp = poke_client.get_pokemon(pokemon_name)
    assert resp.status_code == 200
    data = resp.json()

    stats = data["stats"]
    assert isinstance(stats, list), f"{pokemon_name} has non-list stats: {stats}"
    assert len(stats) > 0, f"{pokemon_name} has no stats defined"

    allowed_names = {
        "hp",
        "attack",
        "defense",
        "special-attack",
        "special-defense",
        "speed",
    }

    for stat_entry in stats:
        name = stat_entry["stat"]["name"]
        assert name in allowed_names, (
            f"{pokemon_name} has unexpected stat name '{name}'. "
            f"Expected one of: {allowed_names}"
        )
