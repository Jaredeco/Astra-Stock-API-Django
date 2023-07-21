from django.urls import path
from .views import BondListView, BondCRUDView, BondCreateView, AnalyzePortfolioView, AuthenticationView, \
    PurchaseBondView, UserPortfolioBondListView, UserPortfolioInvestmentListView, InvestmentCRUDView

# decided to use trailing slash
urlpatterns = [
    path('authentication/', AuthenticationView.as_view(), name='authentication'),
    path('bonds/', BondListView.as_view(), name='bond-list'),
    path('bond/', BondCreateView.as_view(), name='create-bond'),
    path('bond/<str:isin>/', BondCRUDView.as_view(), name='bond-detail'),
    path('portfolio/', AnalyzePortfolioView.as_view(), name='analyze-portfolio'),
    path('portfolio/investments/', UserPortfolioInvestmentListView.as_view(), name='user-portfolio-'
                                                                                   'investments'),
    path('portfolio/bonds/', UserPortfolioBondListView.as_view(), name='user-portfolio-bonds'),
    path('investment/', PurchaseBondView.as_view(), name='purchase-bond'),
    path('investment/<int:id>/', InvestmentCRUDView.as_view(), name='investment-detail'),
]
