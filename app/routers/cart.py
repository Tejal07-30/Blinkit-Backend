from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Cart, CartItem, Item
from app.schemas import CartItemAdd, CartItemUpdate, CartResponse
from app.auth_utils import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


def get_user_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def build_cart_response(cart: Cart) -> CartResponse:
    items_out = []
    total = 0.0
    for ci in cart.cart_items:
        line_total = ci.item.price * ci.quantity
        total += line_total
        items_out.append({"item": ci.item, "quantity": ci.quantity, "line_total": line_total})
    return CartResponse(items=items_out, total=total)


@router.get("/", response_model=CartResponse)
def view_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_user_cart(db, current_user.id)
    return build_cart_response(cart)


@router.post("/items", response_model=CartResponse)
def add_to_cart(data: CartItemAdd, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_user_cart(db, current_user.id)

    item = db.query(Item).filter(Item.id == data.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.item_id == data.item_id).first()
    total_quantity = data.quantity + (existing.quantity if existing else 0)

    if total_quantity > item.stock:
        raise HTTPException(status_code=400, detail=f"Only {item.stock} unit(s) of '{item.name}' available")

    if existing:
        existing.quantity = total_quantity
    else:
        db.add(CartItem(cart_id=cart.id, item_id=data.item_id, quantity=total_quantity))

    db.commit()
    db.refresh(cart)
    return build_cart_response(cart)


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(item_id: int, data: CartItemUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_user_cart(db, current_user.id)
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.item_id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    item = db.query(Item).filter(Item.id == item_id).first()
    if data.quantity > item.stock:
        raise HTTPException(status_code=400, detail=f"Only {item.stock} unit(s) of '{item.name}' available")

    cart_item.quantity = data.quantity
    db.commit()
    db.refresh(cart)
    return build_cart_response(cart)


@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_from_cart(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_user_cart(db, current_user.id)
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.item_id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return build_cart_response(cart)


@router.delete("/")
def clear_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_user_cart(db, current_user.id)
    for ci in cart.cart_items:
        db.delete(ci)
    db.commit()
    return {"message": "Cart cleared"}
