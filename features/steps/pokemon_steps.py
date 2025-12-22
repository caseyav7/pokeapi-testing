from behave import when, then
from src.api_client import PokeApiClient

def get_client(context) -> PokeApiClient:
    if not hasattr(context, "poke_client"):
        context.poke_client = PokeApiClient()
    return context.poke_client


@when("I request the default Pokemon list")
def step_request_default_list(context):
    client = get_client(context)
    context.response = client.get_pokemon_list()


@when('I request the Pokemon list with limit "{limit}" and offset "{offset}"')
def step_request_pokemon_list_with_pagination(context, limit, offset):
    client = get_client(context)
    context.response = client.get_pokemon_list(limit=int(limit), offset=int(offset))


@when('I request the Pokemon with name "{name}"')
def step_request_pokemon_by_name(context, name):
    client = get_client(context)
    context.response = client.get_pokemon(name)


@when('I request the Pokemon with id "{pokemon_id}"')
def step_request_pokemon_by_id(context, pokemon_id):
    client = get_client(context)
    context.response = client.get_pokemon(pokemon_id)


@then("the response status code should be {status_code:d}")
def step_check_status_code(context, status_code):
    assert context.response.status_code == status_code, (
        f"Expected {status_code}, got {context.response.status_code}. "
        f"Body: {context.response.text}"
    )


@then('the response should contain a non-empty "results" array')
def step_check_results_array(context):
    body = context.response.json()
    assert "results" in body, f"No 'results' in body: {body}"
    assert isinstance(body["results"], list), "'results' is not a list"
    assert len(body["results"]) > 0, "'results' is empty"


@then('the response should contain exactly {expected_count:d} results')
def step_check_exact_results_count(context, expected_count):
    body = context.response.json()
    results = body.get("results")
    assert isinstance(results, list), f"'results' is not a list: {results}"
    assert len(results) == expected_count, (
        f"Expected {expected_count} results, got {len(results)}"
    )


@then('the response JSON "name" field should be "{expected_name}"')
def step_check_name_field(context, expected_name):
    body = context.response.json()
    actual = body.get("name")
    assert actual == expected_name, f"Expected name '{expected_name}', got '{actual}'"


@then('the response JSON "id" field should be {expected_id:d}')
def step_check_id_field(context, expected_id):
    body = context.response.json()
    actual = body.get("id")
    assert actual == expected_id, f"Expected id {expected_id}, got {actual}"


@when('I request the Pokemon list with limit "10" and offset "0"')
def step_request_first_page(context):
    client = get_client(context)
    context.first_page = client.get_pokemon_list(limit=10, offset=0)


@when('I request the Pokemon list with limit "10" and offset "10"')
def step_request_second_page(context):
    client = get_client(context)
    context.second_page = client.get_pokemon_list(limit=10, offset=10)


@then('the two Pokemon result sets should not overlap')
def step_check_no_overlap(context):
    body1 = context.first_page.json()
    body2 = context.second_page.json()

    names1 = {p["name"] for p in body1.get("results", [])}
    names2 = {p["name"] for p in body2.get("results", [])}

    overlap = names1 & names2
    assert not overlap, f"Expected no overlap, but found: {overlap}"