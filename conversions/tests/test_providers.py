from datetime import date
import json
from unittest import mock

from django.test import TestCase

from ..providers import FixerExchangeRateProvider
from .. import models as conversion_models
from .mock_fixer_api import mock_fixer_api

# Create your tests here.


@mock.patch('requests.get', mock_fixer_api)
class FixerProviderTestCase(TestCase):
    def setUp(self):
        self.from_currency = 'EUR'
        self.to_currency = 'EGP'
        self.amount = 2.0
        self.rates = {"AED": 105.168752, "AFN": 104.900894, "ALL": 121.441034, "AMD": 546.954659, "ANG": 2.053617, "AOA": 598.962712, "ARS": 120.803029, "AUD": 1.590442, "AWG": 2.043175, "AZN": 1.933903, "BAM": 1.955847, "BBD": 2.30072, "BDT": 97.967634, "BGN": 1.948435, "BHD": 0.427904, "BIF": 2276.819393, "BMD": 1.13494, "BND": 1.531713, "BOB": 7.845367, "BRL": 5.962951, "BSD": 1.13951, "BTC": 2.6672517e-05, "BTN": 85.75283, "BWP": 13.120212, "BYN": 2.913125, "BYR": 22244.817475, "BZD": 2.29692, "CAD": 1.445448, "CDF": 2286.90384, "CHF": 1.051115, "CLF": 0.033151, "CLP": 914.725391, "CNY": 7.212092, "COP": 4471.338086, "CRC": 732.476239, "CUC": 1.13494, "CUP": 30.075901, "CVE": 110.265939, "CZK": 24.563844, "DJF": 202.861728, "DKK": 7.440329, "DOP": 65.155555, "DZD": 159.834734, "EGP": 17.832152, "ERN": 17.024117, "ETB": 57.342188, "EUR": 1, "FJD": 2.422533, "FKP": 0.826145, "GBP": 0.836822, "GEL": 3.325817, "GGP": 0.826145, "GHS": 7.304162, "GIP": 0.826145, "GMD": 60.26967, "GNF": 10274.787518, "GTQ": 8.762675, "GYD": 238.402031, "HKD": 8.85308, "HNL": 28.055239, "HRK": 7.531505, "HTG": 116.497992, "HUF": 356.450941, "IDR": 16280.425789, "ILS": 3.672257, "IMP": 0.826145, "INR": 85.516006, "IQD": 1663.084166, "IRR": 47951.201335, "ISK": 141.890595, "JEP": 0.826145, "JMD": 179.104526, "JOD": 0.804717, "JPY": 131.536147, "KES": 129.446003, "KGS": 96.22541, "KHR": 4636.539493, "KMF": 490.351119, "KPW": 1021.445879, "KRW": 1361.694983, "KWD": 0.343036, "KYD": 0.949608, "KZT": 490.034174, "LAK": 12944.610258,
                      "LBP": 1723.114677, "LKR": 230.746665, "LRD": 174.331017, "LSL": 17.274215, "LTL": 3.351182, "LVL": 0.686514, "LYD": 5.221644, "MAD": 10.640891, "MDL": 20.282873, "MGA": 4538.018654, "MKD": 61.630525, "MMK": 2026.069857, "MNT": 3244.60089, "MOP": 9.154978, "MRO": 405.173266, "MUR": 49.660423, "MVR": 17.535247, "MWK": 913.243779, "MXN": 23.317166, "MYR": 4.754834, "MZN": 72.443627, "NAD": 17.27421, "NGN": 473.281618, "NIO": 40.400344, "NOK": 10.093477, "NPR": 137.204169, "NZD": 1.706805, "OMR": 0.436974, "PAB": 1.13951, "PEN": 4.260936, "PGK": 4.035734, "PHP": 58.185496, "PKR": 199.011895, "PLN": 4.572613, "PYG": 7942.967656, "QAR": 4.132359, "RON": 4.945958, "RSD": 117.557475, "RUB": 87.15588, "RWF": 1184.520089, "SAR": 4.258075, "SBD": 9.178684, "SCR": 14.852127, "SDG": 502.214977, "SEK": 10.603413, "SGD": 1.52957, "SHP": 1.56327, "SLL": 13068.830651, "SOS": 662.80515, "SRD": 23.11309, "STD": 23490.959675, "SVC": 9.971085, "SYP": 2850.968189, "SZL": 17.247647, "THB": 37.128459, "TJS": 12.87051, "TMT": 3.972289, "TND": 3.273209, "TOP": 2.573987, "TRY": 15.344502, "TTD": 7.744366, "TWD": 31.675074, "TZS": 2635.64245, "UAH": 31.930172, "UGX": 4013.234184, "USD": 1.13494, "UYU": 49.28342, "UZS": 12364.87532, "VEF": 242684401354.12613, "VND": 25748.943697, "VUV": 129.010197, "WST": 2.964852, "XAF": 655.962587, "XAG": 0.0504, "XAU": 0.000628, "XCD": 3.067232, "XDR": 0.811707, "XOF": 655.962587, "XPF": 119.679801, "YER": 284.019065, "ZAR": 17.270026, "ZMK": 10215.823009, "ZMW": 21.376782, "ZWL": 365.45011}

    def test_provider_can_fetch_from_api(self):
        # This makes an external call to the API which is counted towards the quota
        today_rates = conversion_models.DateExchangeRates.objects.filter(
            date_created=date.today()).first()
        self.assertIsNone(today_rates, 'Today rates object already exists.')
        FixerExchangeRateProvider()
        today_rates = conversion_models.DateExchangeRates.objects.filter(
            date_created=date.today()).first()
        self.assertIsNotNone(today_rates, 'Could not fetch data')

    def test_provider_uses_db_rates_if_exists(self):
        today_rates = conversion_models.DateExchangeRates.objects.create(
            rates=self.rates)
        provider = FixerExchangeRateProvider()
        self.assertEqual(json.loads(today_rates.rates), provider.rates)

    def test_rate_conversion(self):
        rates = {"EGP": 2, "EUR": 1, "USD": 4}
        from_currency = "USD"
        to_currency = "EGP"
        conversion_models.DateExchangeRates.objects.create(
            rates=rates)
        provider = FixerExchangeRateProvider()
        provider_rate = provider.rate_from_to(from_currency, to_currency)
        calculated_rate = rates.get(to_currency)/rates.get(from_currency)
        self.assertEqual(provider_rate, calculated_rate)

    def test_conversion(self):
        rates = {"EGP": 2, "EUR": 1, "USD": 4}
        from_currency = "USD"
        to_currency = "EGP"
        amount = 2.0
        conversion_models.DateExchangeRates.objects.create(
            rates=rates)
        provider = FixerExchangeRateProvider()
        provider_amount = provider.convert(from_currency, to_currency, amount)
        calculated_amount = provider.rate_from_to(
            from_currency, to_currency) * amount
        self.assertEqual(provider_amount, calculated_amount)
