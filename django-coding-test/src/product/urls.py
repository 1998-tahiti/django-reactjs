from django.urls import path
from django.views.generic import TemplateView
from product.views.product import EditProductView
from product.views.product import CreateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView
from product.views.product import ProductFilterView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'product': True
    }), name='list.product'),
    path('api/product-filter/', ProductFilterView.as_view(), name='product_filter'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='edit_product'),
]



