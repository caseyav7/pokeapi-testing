from behave import when, then
from src.api_client import PokeApiClient

# We can reuse one client for all steps in a scenario
def get_client(context) -> PokeApiClient:
    if not hasattr(context, "poke_client"):
        context.poke_client = PokeApiClient()
    return context.poke_client


@when("I request the default Pokemon list")
def step_request_default_list(context):
    client = get_client(context)
    context.response = client.get_pokemon_list()


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