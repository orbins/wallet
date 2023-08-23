from django.urls import path, include

from .routers import goals_router
from .views.dashboard import DashboardView

urlpatterns = [
    path(
        'dashboard/',
        DashboardView.as_view(),
        name='dashboard',
    ),
    path('', include(goals_router.urls)),
]
