from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from ..models import Quote
from ..serializers import QuoteSerializer


class QuoteCreateRetriveView(APIView):
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'post')

    def get(self, request):
        quote = Quote.objects.filter(user=self.request.user).order_by('?').first()
        if quote:
            serializer = QuoteSerializer(quote)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Вы не добавляли цитат"}
            )

    def post(self, request):
        serializer = QuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
