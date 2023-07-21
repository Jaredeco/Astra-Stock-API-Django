from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import requests


def _validate_isin(isin):
    url = "https://www.cdcp.cz/isbpublicjson/api/VydaneISINy"
    params = {"isin": isin}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValidationError(response.json()['message'])


# Set null=True to make sure there are no db conflicts, remove null=True if database is clean
class Bond(models.Model):
    name = models.CharField(max_length=100, null=True)
    isin = models.CharField(max_length=12, unique=True, null=True, validators=[_validate_isin])
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True, null=True)
    expiration_date = models.DateTimeField(null=True)
    interest_payment_frequency = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.name} ({self.isin})"


class Investment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', null=True)
    bond_isin = models.ForeignKey(Bond, on_delete=models.CASCADE, to_field='isin', null=True)
    volume = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.username.username} - {self.bond_isin.name} ({self.volume})"
