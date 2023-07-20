from django.urls import path
from .views import BondListView, BondCRUDView, BondCreateView, AnalyzePortfolioView, AuthenticationView, \
    PurchaseBondView, UserPortfolioBondListView, UserPortfolioInvestmentListView

urlpatterns = [
    path('authentication/', AuthenticationView.as_view(), name='authentication'),
    path('bonds/', BondListView.as_view(), name='bond-List'),
    path('bond/', BondCreateView.as_view(), name='create-Bond'),
    path('bond/<str:isin>/', BondCRUDView.as_view(), name='bond-Detail'),
    path('portfolio/<str:username>/', AnalyzePortfolioView.as_view(), name='analyze-portfolio'),
    path('portfolio/investments/<str:username>/', UserPortfolioInvestmentListView.as_view(), name='user portfolio '
                                                                                                  'investments'),
    path('portfolio/bonds/<str:username>/', UserPortfolioBondListView.as_view(), name='user portfolio bonds'),
    path('investment/', PurchaseBondView.as_view(), name='purchase-bond'),
]
