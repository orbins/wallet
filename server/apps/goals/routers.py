from rest_framework.routers import DefaultRouter

from .viewsets import GoalViewSet

goals_router = DefaultRouter()

goals_router.register(
    prefix='mine',
    viewset=GoalViewSet,
    basename='goals',
)
