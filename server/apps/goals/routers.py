from rest_framework.routers import DefaultRouter

from .viewsets import GoalViewSet

goals_router = DefaultRouter()

goals_router.register(
    prefix='goals',
    viewset=GoalViewSet,
    basename='goals',
)
