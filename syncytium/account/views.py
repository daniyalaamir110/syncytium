from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import UserSerializer
from .models import UserPrivacy


class UserCreateAPIView(CreateAPIView):
    """
    API view to create a new user.
    """

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        serializer.save()
        user = serializer.instance
        user.set_password(password)
        user.save()
        UserPrivacy.objects.create(user=user)
        return user
