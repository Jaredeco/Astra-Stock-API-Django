from rest_framework import serializers
from base.models import Bond, Investment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
