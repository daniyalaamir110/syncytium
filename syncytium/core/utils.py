from cities_light.models import City, Country
from django.core.exceptions import ValidationError


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
