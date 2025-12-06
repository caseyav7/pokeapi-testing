# <img width="34" height="34" alt="poke_pika" src="https://github.com/user-attachments/assets/fb1bafa1-5e92-4369-bdcb-eb934510173f" /> PokeAPI Testing Project

This project demonstrates API testing using **pytest**, **Python requests**, and **PokeAPI** — a large, fun, public REST API based on Pokémon data.

It includes:

- Pokémon list endpoint (`/pokemon`)
- Pagination testing
- Pokémon detail endpoint (`/pokemon/{name or id}`)
- Data validation for types, structure, and required fields
- Negative test cases (404s, invalid parameters)
- A reusable API client wrapper
- **Optional BDD (Behavior-Driven Development) tests using Gherkin + Behave**

---

## 🚀 Installing Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the Pytest Test Suite

Run all API tests written with pytest:

```bash
pytest -vv
```

This will execute:

- `test_pokemon_list.py`
- `test_single_pokemon.py`
- `test_negative_pokemon.py`

---

## 🌿 Running the BDD Test Suite (Behave)

This project also includes optional **BDD-style tests** using Gherkin scenarios and Behave step definitions.

To run the Behave suite:

```bash
behave
```

Behave will automatically load:

- `features/pokemon_api.feature`
- Step files in `features/steps/`

### ✔ What the BDD Scenarios Cover

- Fetching the default Pokémon list
- Validating list structure (non-empty results)
- Fetching Pokémon by **name** (Pikachu, Bulbasaur, Charmander)
- Fetching Pokémon by **ID** (1, 4, 25)
- Negative scenario: requesting a non-existent Pokémon

---

## 📂 Project Structure

```
pokeapi-testing/
├── README.md
├── requirements.txt
├── pytest.ini
│
├── src/
│   └── api_client.py
│
├── tests/
│   ├── conftest.py
│   ├── test_pokemon_list.py
│   ├── test_single_pokemon.py
│   └── test_negative_pokemon.py
│
├── features/
│   ├── pokemon_api.feature
│   └── steps/
│       ├── pokemon_steps.py
│       └── __init__.py
│
└── behave.ini
```
