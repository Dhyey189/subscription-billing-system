import stripe
from users.models import User


def get_or_create_stripe_customer(user: User):
    """
    Create customer record on stripe and stores stripe_customer_id in User model.
    """
    if user.stripe_customer_id:
        return stripe.Customer.retrieve(user.stripe_customer_id)

    stripe_customer = stripe.Customer.create(
        email=user.email,
        name=user.name,
    )
    user.stripe_customer_id = stripe_customer.id
    user.save()

    return stripe_customer
