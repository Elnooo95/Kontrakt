from fastapi import APIRouter, Depends, HTTPException, Request
from ..config import settings
from ..security import get_current_user_id
import stripe

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/create-checkout-session")
def create_checkout_session(user_id: int = Depends(get_current_user_id)):
    if not (settings.STRIPE_SECRET_KEY and settings.STRIPE_PRICE_ID and settings.STRIPE_SUCCESS_URL and settings.STRIPE_CANCEL_URL):
        raise HTTPException(status_code=500, detail="Stripe är inte konfigurerat")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )
    return {"url": session.url}

@router.post("/webhook")
async def webhook(request: Request):
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Stripe webhook saknas")
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig, secret=settings.STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # TODO: koppla event till användare och uppdatera subscription_status
    return {"received": True}
