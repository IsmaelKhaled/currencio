from rest_framework import serializers

from . import enums as conversion_enums


class ConversionSerializer(serializers.Serializer):
    from_currency = serializers.ChoiceField(
        choices=conversion_enums.CurrencyChoices.choices())
    to_currency = serializers.ChoiceField(
        choices=conversion_enums.CurrencyChoices.choices())
    amount = serializers.FloatField()
