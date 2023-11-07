from django.urls import path

from ..quotes.views import QuoteCreateRetriveView

urlpatterns = [
    path('', QuoteCreateRetriveView.as_view()),
]
