# <img width="44" height="44" alt="poke_pika" src="https://github.com/user-attachments/assets/fb1bafa1-5e92-4369-bdcb-eb934510173f" /> PokeAPI Testing Project

This project demonstrates API testing using **pytest**, **Python requests**, and **PokeAPI** — a large, fun, public REST API based on Pokémon data.

It covers:

- Pokémon list endpoint (`/pokemon`)
- Pagination testing
- Pokémon detail endpoint (`/pokemon/{name or id}`)
- Data validation for types, structure, and required fields
- Negative test cases (404s, invalid parameters)
- A reusable API client wrapper

---

## 🚀 Running the tests


Install dependencies:

```bash
pip install -r requirements.txt

Run all tests:
pytest -vv
