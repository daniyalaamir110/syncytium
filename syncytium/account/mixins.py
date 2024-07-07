from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS


class MustExistForUsernameAPIMixin:
    """Check if the detail object exists.

    Preconditions:
    - The `model` attribute must be defined in the view.
    
    Operations:
    - In case of read-only methods, if the object does not exist, raise a 404 error.
    - In case of write methods, if the object does not exist, create it if `create` is `True`.
    """

    def get_object(self, create=False):
        username = self.kwargs.get("username")
        try:
            return self.model.objects.get(user__username=username)
        except self.model.DoesNotExist:
            if self.request.method in SAFE_METHODS or not create:
                raise NotFound
            return self.model(user_id=self.request.user.id)
