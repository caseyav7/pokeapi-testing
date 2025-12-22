from behave import when, then
from src.api_client import PokeApiClient

def get_client(context) -> PokeApiClient:
    if not hasattr(context, "poke_client"):
        context.poke_client = PokeApiClient()
    return context.poke_client

@when('I request the Pokemon with name "{name}"')
def step_request_pokemon_by_name(context, name):
    client = get_client(context)
    context.response = client.get_pokemon(name)

@when("I request the default Pokemon list")
def step_request_default_list(context):
    client = get_client(context)
    context.response = client.get_pokemon_list()

@when('I request the Pokemon list with limit "{limit}" and offset "{offset}"')
def step_request_pokemon_list_with_pagination(context, limit, offset):
    client = get_client(context)
    resp = client.get_pokemon_list(limit=int(limit), offset=int(offset))
    context.response = resp

    if not hasattr(context, "list_responses"):
        context.list_responses = []
    context.list_responses.append(resp)

@when('I request an invalid Pokemon name of "{name}"')
def step_request_invalid_pokemon_name(context, name):
    client = get_client(context)

    # Safe tokens for whitespace cases
    if name == "<SPACE>":
        name = " "
    elif name == "<TRIPLE_SPACE>":
        name = "   "

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

@then('the two Pokemon result sets should not overlap')
def step_check_no_overlap(context):
    assert hasattr(context, "list_responses"), "No stored list responses. Did you request two pages?"
    assert len(context.list_responses) >= 2, "Need at least two list responses to compare."

    resp1 = context.list_responses[-2]
    resp2 = context.list_responses[-1]

    body1 = resp1.json()
    body2 = resp2.json()

    names1 = {p["name"] for p in body1.get("results", [])}
    names2 = {p["name"] for p in body2.get("results", [])}

    overlap = names1 & names2
    assert not overlap, f"Expected no overlap, but found: {overlap}"