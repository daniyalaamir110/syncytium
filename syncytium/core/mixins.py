from rest_framework.views import Http404


class MustExistForUsernameAPIMixin:
    """
    Mixin to check if the detail object exists.
    If the object does not exist, raise a 404 error.
    """

    def does_exist(self):
        obj = self.get_object()
        if obj is None:
            raise Http404
        return obj
