import requests
import json
from datetime import date

from django.conf import settings

from .models import DateExchangeRates


class FixerExchangeRateProvider:
    """ 
    A provider to fetch exchange rates from a 3rd party API and return the required exchange rate between currencies
    """

    def __init__(self):
        self.rates = None
        self.get_exchange_rates()

    def get_exchange_rates(self):
        try:
            # First try to retrieve today's rates from the database
            today_rates = DateExchangeRates.objects.get(
                date_created=date.today())
            self.rates = json.loads(today_rates.rates)
        except DateExchangeRates.DoesNotExist:
            # If today rates don't exist in the DB, make a new request to the 3rd party API and save it to the DB
            api_url = f'{settings.FIXER_BASE_URL}latest?access_key={settings.FIXER_API_KEY}'
            response = requests.get(api_url)
            if response.json().get('success') is True:
                self.rates = response.json().get('rates')
                DateExchangeRates.objects.create(rates=self.rates)
            else:
                raise RuntimeError("Could not fetch exchange rates: %s" %
                                   response.json().get('error').get('info'))

    def rate_from_to(self, base_currency, to_currency):
        eur_to_base = float(self.rates.get(base_currency))
        eur_to_sought = float(self.rates.get(to_currency))
        return float(eur_to_sought / eur_to_base)

    def convert(self, from_currency, to_currency, amount):
        rate = self.rate_from_to(from_currency, to_currency)
        return float(rate * amount)
