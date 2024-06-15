from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from account.serializers import UserSerializer


class CurrentUserRetrieveAPIView(RetrieveAPIView):
    """
    API view to retrieve the current user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=False, methods=["GET"])
    def retrieve(self, request):
        user = self.get_serializer(request.user).data
        return Response(user, status=HTTP_200_OK)
