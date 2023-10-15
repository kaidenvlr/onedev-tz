from drf_yasg import openapi

user_id_parameter = openapi.Parameter(
    name='user_id',
    in_=openapi.IN_QUERY,
    description="User ID to Fetch",
    type=openapi.TYPE_INTEGER
)
