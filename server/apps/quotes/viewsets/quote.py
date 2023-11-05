from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import Quote
from ..serializers import QuoteSerializer


class QuoteViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = QuoteSerializer

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user)

    def get_object(self):
        return Quote.objects.get(user=self.request.user).order_by('?').first()

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
