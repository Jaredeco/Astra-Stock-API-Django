from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Bond, Investment


class BondModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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
