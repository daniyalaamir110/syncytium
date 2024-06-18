from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings


def validate_country_and_city(country, city):
    """
    Validate country and city.
    Check if the city belongs to the country.
    """

    if not country:
        country = city.country
    elif city.country != country:
        raise ValidationError("City does not belong to the country")
    return country, city


def send_email(subject="", message="", recipient_list=[]):
    """
    Send email.
    """
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return True
