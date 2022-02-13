from django.contrib import admin

from conversions.models import ConversionCount, DateExchangeRates

# Register your models here.


@admin.register(ConversionCount)
class ConversionCountAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'count')
    list_filter = ('from_currency', 'to_currency')


@admin.register(DateExchangeRates)
class DateExchangeRatesAdmin(admin.ModelAdmin):
    list_display = ('date_created',)
