from secrets import token_hex

from .models import UserEmailStatus


def generate_email_verification_token(user_id):
    """
    Generate an email verification token for the user.
    Whenever a user changes their email address, a new token is generated,
    and the previous token is invalidated.
    """
    email_status = UserEmailStatus.objects.get_or_create(user_id=user_id)[0]
    email_status.verification_token = token_hex(16)
    email_status.is_verified = False
    email_status.save()
    return email_status.verification_token
