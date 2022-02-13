import enum


class CurrencyChoices(enum.Enum):
    EGP = "EGP"
    EUR = "EUR"
    USD = "USD"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
