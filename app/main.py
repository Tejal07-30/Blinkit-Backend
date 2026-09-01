from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, items, cart, wallet

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blinkit Backend")

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(cart.router)
app.include_router(wallet.router)


@app.get("/")
def root():
    return {"message": "Blinkit backend is running"}
