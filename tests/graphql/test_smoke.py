import os
import pytest
from src.graphql_client import PokeGraphQLClient

RUN_INTEGRATION = os.getenv("RUN_INTEGRATION_TESTS", "").lower() in {"1", "true", "yes"}

@pytest.mark.integration
@pytest.mark.skipif(not RUN_INTEGRATION, reason="Set RUN_INTEGRATION_TESTS=1 to run live API tests")
def test_graphql_smoke_typename():
    client = PokeGraphQLClient()

    resp = client.query("query Smoke { __typename }")

    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:500]}"

    payload = resp.json()
    assert isinstance(payload, dict)
    assert "data" in payload, f"Missing data key. Payload: {payload}"
    assert not payload.get("errors"), f"GraphQL errors: {payload.get('errors')}"
    assert payload["data"]["__typename"], f"Unexpected data: {payload['data']}"


@pytest.mark.integration
@pytest.mark.skipif(not RUN_INTEGRATION, reason="Set RUN_INTEGRATION_TESTS=1 to run live API tests")
def test_graphql_smoke_bad_query_returns_errors():
    """Negative smoke test: API is reachable and returns a GraphQL `errors` envelope for an invalid query."""

    client = PokeGraphQLClient()

    resp = client.query("query SmokeBad { definitelyNotARealField }")

    # GraphQL commonly returns 200 even when the query is invalid.
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:500]}"

    payload = resp.json()
    assert isinstance(payload, dict)

    # For an invalid query, we expect an errors array.
    assert payload.get("errors"), f"Expected GraphQL errors. Payload: {payload}"


@pytest.mark.integration
@pytest.mark.skipif(not RUN_INTEGRATION, reason="Set RUN_INTEGRATION_TESTS=1 to run live API tests")
def test_graphql_smoke_introspection_querytype():
    """Smoke test: basic GraphQL introspection works and returns a query type name."""

    client = PokeGraphQLClient()

    query = """
    query IntrospectionSmoke {
      __schema {
        queryType {
          name
        }
      }
    }
    """.strip()

    resp = client.query(query)

    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:500]}"

    payload = resp.json()
    assert isinstance(payload, dict)
    assert "data" in payload, f"Missing data key. Payload: {payload}"
    assert not payload.get("errors"), f"GraphQL errors: {payload.get('errors')}"

    query_type_name = payload["data"]["__schema"]["queryType"]["name"]
    assert query_type_name, f"Unexpected introspection response: {payload['data']}"

