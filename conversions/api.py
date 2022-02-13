from django import http
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .providers import FixerExchangeRateProvider
from .serializers import ConversionSerializer
from .models import ConversionCount


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes((IsAuthenticated,))
def conversion_api(request):
    provider = FixerExchangeRateProvider()
    serializer = ConversionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
    converted_amount = provider.convert(**data)

    try:
        count_obj = ConversionCount.objects.get(
            from_currency=data.get('from_currency'),
            to_currency=data.get('to_currency')
        )
        count_obj.increase_count()
    except ConversionCount.DoesNotExist:
        count_obj = ConversionCount.objects.create(
            from_currency=data.get('from_currency'),
            to_currency=data.get('to_currency'),
            count=1
        )

    response = {
        "from_currency": data.get('from_currency'),
        "to_currency": data.get('to_currency'),
        "original_amount": data.get('amount'),
        "converted_amount": converted_amount
    }
    return Response(response, status=status.HTTP_200_OK)
