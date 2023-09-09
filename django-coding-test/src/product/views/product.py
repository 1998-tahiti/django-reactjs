from django.views import generic
from django.http import HttpResponse
from product.models import Variant
from product.models import Product
from django.views.generic import CreateView
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import generics
from product.models import Product, ProductVariant, ProductVariantPrice
from product.serializers import ProductSerializer, ProductVariantSerializer, ProductVariantPriceSerializer
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy



class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'
    paginate_by = 10
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        paginator = Paginator(self.queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = page.object_list
        context['variants'] = list(variants.all())
        return context
    
    def post(self, request, *args, **kwargs):
        product_data = request.POST
        product = Product.objects.create(**product_data)
        return HttpResponse(status=201)
    


class ProductFilterView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        product_title = self.request.query_params.get('product_title')
        product_variant = self.request.query_params.get('product_variant')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if product_title:
            queryset = queryset.filter(title__icontains=product_title)

        if product_variant:
            queryset = queryset.filter(productvariant__variant_title__icontains=product_variant)

        if min_price is not None:
            queryset = queryset.filter(productvariant__productvariantprice__price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(productvariant__productvariantprice__price__lte=max_price)

        if start_date:
            queryset = queryset.filter(productvariant__productvariantprice__created_at__gte=start_date)

        if end_date:
            queryset = queryset.filter(productvariant__productvariantprice__created_at__lte=end_date)

        return queryset
    
class EditProductView(UpdateView):
    model = Product
    # form_class = YourProductFormClass  # Replace with the actual form class you have for editing products
    template_name = 'products/edit.html'  # Create an edit.html template for the edit form
    success_url = reverse_lazy('product_list')  # Redirect to the product list page after successful edit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = Variant.objects.filter(active=True).values('id', 'title')
        return context




