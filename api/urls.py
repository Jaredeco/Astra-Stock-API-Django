from django.urls import path
from .views import astra_products_number, astra_products_names, astra_product_parts

urlpatterns = [
    path('products_number/', astra_products_number, name='products-number'),
    path('products/', astra_products_names, name='products-names'),
    path('product/<product_code>/', astra_product_parts, name='product-parts'),
]
