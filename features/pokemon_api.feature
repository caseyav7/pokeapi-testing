Feature: PokeAPI - Pokemon endpoints
  As a QA engineer
  I want to validate the Pokemon endpoints of PokeAPI
  So that I can ensure basic functionality and responses are correct

  # -------------------------
  # LIST ENDPOINT
  # -------------------------

  Scenario: Get default list of Pokemon
    When I request the default Pokemon list
    Then the response status code should be 200
    And the response should contain a non-empty "results" array

  Scenario Outline: Get Pokemon list with pagination
    When I request the Pokemon list with limit "<limit>" and offset "<offset>"
    Then the response status code should be 200
    And the response should contain exactly <expected_count> results

    Examples:
      | limit | offset | expected_count |
      | 5     | 0      | 5              |
      | 10    | 20     | 10             |
      | 15    | 30     | 15             |

  Scenario: Pokemon list pages should not overlap
    When I request the Pokemon list with limit "10" and offset "0"
    And I request the Pokemon list with limit "10" and offset "10"
    Then the two Pokemon result sets should not overlap

  # -------------------------
  # SINGLE POKEMON
  # -------------------------

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

  # -------------------------
  # NEGATIVE CASES
  # -------------------------

  Scenario Outline: Non-existent Pokemon returns 404
    When I request the Pokemon with name "<name>"
    Then the response status code should be 404

    Examples:
      | name                     |
      | definitely-not-real-9999 |
      | missingno-12345          |

  Scenario Outline: Non-existent Pokemon by id returns 404
    When I request the Pokemon with id "<id>"
    Then the response status code should be 404

    Examples:
      | id     |
      | 999999 |
      | 123456 |

  Scenario Outline: Invalid id formats return 404
    When I request the Pokemon with id "<id>"
    Then the response status code should be 404

    Examples:
      | id  |
      | 0   |
      | -1  |
      | 1.5 |
      | abc |

  Scenario Outline: Invalid name returns 404
    When I request an invalid Pokemon name of "<name>"
    Then the response status code should be 404

    Examples:
      | name       |
      | Pikachu    |
      | pikachu%20 |
      | pika-chu   |
      |  pikachu   |
      | pikachu    |
      | " "        |
      | "   "      |

