from rest_framework.serializers import ModelSerializer

from ..models import Quote


class QuoteSerializer(ModelSerializer):

    class Meta:
        model = Quote
        fields = ('text', )