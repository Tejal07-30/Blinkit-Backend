from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Wallet
from app.schemas import WalletResponse, TopUpRequest
from app.auth_utils import get_current_user

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/", response_model=WalletResponse)
def view_wallet(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    return wallet


@router.post("/topup", response_model=WalletResponse)
def top_up_wallet(data: TopUpRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Top-up amount must be greater than 0")

    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    wallet.balance += data.amount
    db.commit()
    db.refresh(wallet)
    return wallet
