# Blinkit-Style Backend — Phase 1

A simplified quick-commerce backend (auth, wallet, items, cart) built with **FastAPI + PostgreSQL**.

## Why FastAPI + PostgreSQL?

- **FastAPI**: it's Python, gives free interactive API docs at `/docs`, and validates
  request/response data automatically using Pydantic — no extra boilerplate for that.
- **PostgreSQL**: it's relational, which fits well here since wallets, items, carts and
  users all reference each other. Also just a widely used, solid choice for this kind of app.

## Project layout

```
app/
  main.py           -> creates the FastAPI app, includes all routers
  database.py        -> DB connection setup
  models.py          -> all SQLAlchemy tables
  schemas.py          -> all Pydantic request/response models
  auth_utils.py        -> password hashing + JWT + get_current_user
  routers/
    auth.py            -> signup, login, logout, /me
    wallet.py           -> view balance, top-up
    items.py            -> item CRUD
    cart.py              -> add/remove/update/view/clear cart
docker-compose.yml    -> spins up Postgres locally
requirements.txt
```

Kept it flat on purpose — routes and their logic live together in each router file
instead of being split across extra "service" layers, so it's easy to read top to bottom.

## How to run it

1. Start Postgres:
   ```
   docker compose up -d
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy the example env file (defaults already match docker-compose.yml):
   ```
   cp .env.example .env
   ```

4. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

5. Go to `http://localhost:8000/docs` to try it out. Sign up, log in, click
   "Authorize" and paste the token, then try the other endpoints.

## What each part does

**Auth** — signup creates a user + wallet + cart together. Login returns a JWT.
Logout adds the token to an in-memory blacklist (kept simple — see note below).

**Wallet** — every user gets one wallet automatically. Balance can be topped up
(simulated, no real payment) and can never go below 0.

**Items** — basic CRUD. Anyone logged in can add/edit/delete for now — restricting
this to "sellers only" and "only your own items" is a Phase 2 thing (roles).

**Cart** — one cart per user, stored in the DB. Adding an item checks it doesn't
exceed available stock. Total price is calculated fresh every time you view the cart.

## Known limitations (on purpose, for Phase 1 scope)

- Logout uses an in-memory set of blacklisted tokens, so it resets if the server
  restarts. A more permanent solution (DB table or Redis) is easy to add later,
  but felt unnecessary for this phase.
- No role-based permissions yet (`role` and `seller_id` columns exist but aren't
  enforced) — that's Phase 2.
- No search/filter/sort/pagination yet — also Phase 2/3.
- Price/balance are stored as `float`. Floats can have tiny rounding errors with
  money — a production app would use `Decimal` instead. Kept as float here to
  keep things simple; worth mentioning as a known trade-off in the interview.
