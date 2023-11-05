from django.urls import path, include

from .routers import quotes_router

urlpatterns = [
    path('', include(quotes_router.urls)),
]
