Feature: PokeAPI - Pokemon endpoints
  As a QA engineer
  I want to validate the Pokemon endpoints of PokeAPI
  So that I can ensure basic functionality and responses are correct

  Scenario: Get default list of Pokemon
    When I request the default Pokemon list
    Then the response status code should be 200
    And the response should contain a non-empty "results" array

  Scenario Outline: Get Pokemon by name
    When I request the Pokemon with name "<name>"
    Then the response status code should be 200
    And the response JSON "name" field should be "<name>"

    Examples:
      | name       |
      | pikachu    |
      | bulbasaur  |
      | charmander |

  Scenario Outline: Get Pokemon by id
    When I request the Pokemon with id "<id>"
    Then the response status code should be 200
    And the response JSON "id" field should be <id>

    Examples:
      | id |
      | 1  |
      | 4  |
      | 25 |

  Scenario: Non-existent Pokemon should return 404
    When I request the Pokemon with name "definitely-not-real-9999"
    Then the response status code should be 404

  Scenario: Non-existent Pokemon by id returns 404
    When I request the Pokemon with id "999999"
    Then the response status code should be 404