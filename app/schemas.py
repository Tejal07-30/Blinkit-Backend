from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr



class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    class Config:
        from_attributes = True  


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class TopUpRequest(BaseModel):
    amount: float


class WalletResponse(BaseModel):
    balance: float
    currency: str

    class Config:
        from_attributes = True



class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: int = 0
    unit: str = "pcs"
    image_url: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    unit: Optional[str] = None
    image_url: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: int
    unit: str
    image_url: Optional[str] = None
    seller_id: Optional[int] = None

    class Config:
        from_attributes = True



class CartItemAdd(BaseModel):
    item_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    item: ItemResponse
    quantity: int
    line_total: float


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float
