from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Bond, Investment
from unittest.mock import patch
from django.core.exceptions import ValidationError


class BondModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    #optional test, Django already handles this
    def test_create_bond(self):
        # Create a new Bond
        bond = Bond.objects.create(
            name='Test Bond',
            isin='TEST12345678',
            value=1000,
            interest_rate=0.05,
            purchase_date='2023-01-01',
            expiration_date='2024-01-01',
            interest_payment_frequency='Annual',
        )

        # Check if the Bond is created successfully
        self.assertEqual(bond.name, 'Test Bond')
        self.assertEqual(bond.isin, 'TEST12345678')
        self.assertEqual(bond.value, 1000)
        self.assertEqual(bond.interest_rate, 0.05)
        self.assertEqual(bond.expiration_date, '2024-01-01')
        self.assertEqual(bond.interest_payment_frequency, 'Annual')
    
    def test_bond_str_representation(self):
        # Create a new Bond
        bond = Bond.objects.create(
            name='Test Bond',
            isin='TEST12345678',
            value=1000,
            interest_rate=0.05,
            purchase_date='2023-01-01',
            expiration_date='2024-01-01',
            interest_payment_frequency='Annual',
        )

        # Check the string representation of the Bond
        self.assertEqual(str(bond), 'Test Bond (TEST12345678)')

    @patch('requests.get')
    def test_validate_isin(self, mock_get):
        # Test with a valid ISIN
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'isin': 'CZ0003551251',
            'name': 'Some Bond Name',
        }

        # Create a Bond object with a valid ISIN
        valid_bond = Bond(isin='CZ0003551251', name='Valid Bond', value=1000,
                          interest_rate='0.05',
                          purchase_date='2023-01-01',
                          expiration_date='2024-01-01',
                          interest_payment_frequency='Annual',)
        valid_bond.full_clean()  # This should not raise a ValidationError

        # Test with an invalid ISIN
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {
            'message': 'Invalid ISIN',
        }

        # Create a Bond object with an invalid ISIN
        invalid_bond = Bond(isin='INVALIDISIN', name='Invalid Bond', value=1000,
                            interest_rate=0.05,
                            purchase_date='2023-01-01',
                            expiration_date='2024-01-01',
                            interest_payment_frequency='Annual',)
        with self.assertRaises(ValidationError) as context:
            invalid_bond.full_clean()

        self.assertEqual(context.exception.message_dict['isin'][0], 'Invalid ISIN')


class InvestmentModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test Bond
        self.bond = Bond.objects.create(
            name='Test Bond',
            isin='TEST12345678',
            value=1000,
            interest_rate=0.05,
            purchase_date='2023-01-01',
            expiration_date='2024-01-01',
            interest_payment_frequency='Annual',
        )

    #optional test, Django already handles this
    def test_create_investment(self):
        # Create a new Investment
        investment = Investment.objects.create(
            username=self.user,
            bond_isin=self.bond,
            volume=5,
        )

        # Check if the Investment is created successfully
        self.assertEqual(investment.username, self.user)
        self.assertEqual(investment.bond_isin, self.bond)
        self.assertEqual(investment.volume, 5)

    def test_investment_str_representation(self):
        # Create a new Investment
        investment = Investment.objects.create(
            username=self.user,
            bond_isin=self.bond,
            volume=5,
        )

        # Check the string representation of the Investment
        self.assertEqual(str(investment), f'{self.user.username} - {self.bond.name} (5)')
