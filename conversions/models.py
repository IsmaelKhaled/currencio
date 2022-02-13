from datetime import date
import json
from django.db import models

from . import enums as conversion_enums

# Create your models here.


class ConversionCount(models.Model):
    """
    A model that keeps track of the number of times each conversion is made through the conversion API
    """
    from_currency = models.CharField(
        max_length=3, choices=conversion_enums.CurrencyChoices.choices())
    to_currency = models.CharField(
        max_length=3, choices=conversion_enums.CurrencyChoices.choices())
    count = models.PositiveIntegerField(default=0)

    def increase_count(self):
        self.count += 1
        self.save()


class DateExchangeRates(models.Model):
    """
    A model to keep track of Exchange Rates to avoid extra API calls
    """
    date_created = models.DateField()
    # A TextField that contains the JSON exchange rates retreived from the API (to be parsed and retrieve the individual rates)
    # This would be a JSONField if PostgreSQL was used
    rates = models.TextField()

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = date.today()
        if not isinstance(self.rates, str):
            self.rates = json.dumps(self.rates)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Date Exchange Rates"
