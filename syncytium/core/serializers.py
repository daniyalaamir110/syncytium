from rest_framework.serializers import ModelSerializer
from cities_light.models import Country, Region, City


class CountrySerializer(ModelSerializer):
    """
    Serializer for the Country model.
    """

    class Meta:
        model = Country
        fields = ["id", "name"]


class RegionSerializer(ModelSerializer):
    """
    Serializer for the Region model.
    """

    class Meta:
        model = Region
        fields = ["id", "name"]


class CitySerializer(ModelSerializer):
    """
    Serializer for the City model.
    """

    class Meta:
        model = City
        fields = ["id", "name"]
