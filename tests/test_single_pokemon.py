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