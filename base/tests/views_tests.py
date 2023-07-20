from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Bond, Investment
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "../../bond_service/settings.py")


class ViewsTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a user for testing
        User.objects.create_user(username='testuser2', password='testpassword')

        # Create a bond for testing
        self.bond = Bond.objects.create(
            name='Test Bond',
            isin='TEST12345678',
            value=1000,
            interest_rate=0.05,
            purchase_date='2023-01-01',
            expiration_date='2024-01-01',
            interest_payment_frequency='Annual',
        )

        # Create second bond for testing
        self.bond1 = Bond.objects.create(
            name='Test Bond 2',
            isin='TEST12345679',
            value=2000,
            interest_rate=0.03,
            purchase_date='2023-02-02',
            expiration_date='2024-02-02',
            interest_payment_frequency='Annual',
        )

        self.investment = Investment.objects.create(
            username=self.user,
            bond_isin=self.bond,
            volume=2,
        )

        self.investment1 = Investment.objects.create(
            username=self.user,
            bond_isin=self.bond1,
            volume=7,
        )

    def test_authentication_view(self):
        # Test the AuthenticationView with valid credentials
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post('/api/v1/authentication/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # Test the AuthenticationView with missing credentials
        data = {}
        response = self.client.post('/api/v1/authentication/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username, password', response.data)

    def test_analyze_portfolio_view(self):
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test the AnalyzePortfolioView
        response = self.client.get(f'/api/v1/portfolio/{self.user.username}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_interest_rate', response.data)
        self.assertIn('soon_expires', response.data)
        self.assertIn('portfolio_balance', response.data)
        self.assertIn('future_portfolio_balance', response.data)

    def test_purchase_bond_view(self):
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test the PurchaseBondView with valid data
        data = {
            'username': self.user.username,
            'bond_isin': self.bond.isin,
            'volume': 5,
        }
        response = self.client.post('/api/v1/investment/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('bond_isin', response.data)
        self.assertIn('volume', response.data)

        # Test the PurchaseBondView with invalid volume (<= 0)
        data['volume'] = 0
        response = self.client.post('/api/v1/investment/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_bond_isin_purchase(self):
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test the PurchaseBondView with an invalid bond ISIN
        data = {
            'username': self.user.username,
            'bond_isin': 'INVALID12345678',
            'volume': 5,
        }
        response = self.client.post('/api/v1/investment/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_invalid_user_purchase(self):
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test the PurchaseBondView with an invalid user
        data = {
            'username': 'invaliduser',
            'bond_isin': self.bond.isin,
            'volume': 5,
        }
        response = self.client.post('/api/v1/investment/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_bond_list_view(self):
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test the BondListView
        response = self.client.get('/api/v1/bonds/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_bond_crud_view(self):
        # Authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Test the BondCreateView with valid data
        data = {
            'name': 'New Bond',
            'isin': 'NEW12345678',
            'value': 2000,
            'interest_rate': 0.06,
            'purchase_date': '2023-02-01',
            'expiration_date': '2025-02-01',
            'interest_payment_frequency': 'Semi-Annual',
        }
        response = self.client.post('/api/v1/bond/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)
        self.assertIn('isin', response.data)
        self.assertIn('value', response.data)
        # Add assertions for other fields if needed

        # Test the BondCRUDView (Retrieve)
        response = self.client.get(f'/api/v1/bond/{self.bond.isin}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.bond.name)

        # Test the BondCRUDView (Update)
        data = {
            'name': 'Updated Bond',
            'value': 1500,
        }
        response = self.client.put(f'/api/v1/bond/{self.bond.isin}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Bond')
        self.assertEqual(response.data['value'], '1500.00')

        data = {
            'name': 'Patch Bond',
            'value': 1300,
        }
        response = self.client.patch(f'/api/v1/bond/{self.bond.isin}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patch Bond')
        self.assertEqual(response.data['value'], '1300.00')

        # Test the BondCRUDView (Delete)
        response = self.client.delete(f'/api/v1/bond/{self.bond.isin}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the Bond is deleted
        response = self.client.get(f'/api/v1/bond/{self.bond.isin}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_portfolio_bond_list_view(self):
        # Authenticate the user
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Test the UserPortfolioBondListView
        response = client.get(f'/api/v1/portfolio/bonds/{self.user.username}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure we get both bonds in the user's portfolio
        self.assertIn(self.bond.isin, [item['isin'] for item in response.data])
        self.assertIn(self.bond1.isin, [item['isin'] for item in response.data])

    def test_user_portfolio_investment_list_view(self):
        # Authenticate the user
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Test the UserPortfolioInvestmentListView
        response = client.get(f'/api/v1/portfolio/investments/{self.user.username}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure we get both investments in the user's portfolio
        self.assertIn(self.investment.id, [item['id'] for item in response.data])
        self.assertIn(self.investment1.id, [item['id'] for item in response.data])
