from database import session
from database.model import Gift
from middleware.stripe import get_status

gifts = session.query(Gift).where(Gift.quantity == 0)
for gift in gifts:
    if get_status(gift.stripe_id) == 'succeeded':
        gift.quantity = 1
        print(f'Updated gift {gift.stripe_id} quantity to 1.')
session.commit()
