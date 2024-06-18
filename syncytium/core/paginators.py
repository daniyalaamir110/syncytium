from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom pagination class to limit the number of objects returned.
    """

    default_limit = 10
    max_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"
