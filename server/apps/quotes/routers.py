from rest_framework.routers import DefaultRouter

from .viewsets import QuoteViewSet

quotes_router = DefaultRouter()

quotes_router.register(
    prefix='',
    viewset=QuoteViewSet,
    basename='qoutes',
)
