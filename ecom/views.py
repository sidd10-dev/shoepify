from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.utils import timezone
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,TemplateView,DetailView
# ClassBasedViews
class CategoryPage(ListView):
    model = Category
    template_name = "category_page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orderr = Order.objects.filter(user = self.request.user,complete = False)
        if orderr.exists():
            order = orderr[0]
            orderproduct = OrderProduct.objects.filter(order = order)
            total = 0
            for op in orderproduct:
                amount = op.calcprice()
                total = total + amount
            context['total'] = total
            context['orderproduct'] = orderproduct
            context["count"] = OrderProduct.objects.filter(order = order).count()
        else:
            context["count"] = 0
        context["categories"] = Category.objects.all
        return context
class ProductsPage(ListView):
    model = CategoryBrand
    template_name = "product_page.html"       
    def get_context_data(self,**kwargs):
        slug = self.kwargs.get("slug")
        context = super().get_context_data(**kwargs)
        brands = []
        brandcategory = []
        user = self.request.user
        orderr = Order.objects.filter(user = user,complete = False)
        category = get_object_or_404(Category, slug=slug)
        for i in Brand.objects.all():
            brand_name = i.brand_name+" "+ category.category_name
            for j in CategoryBrand.objects.all():
                if brand_name == j.__str__():
                    brands.append(i)
                    brandcategory.append(j)
        if orderr.exists():
            order = orderr[0]
            orderproduct = OrderProduct.objects.filter(order = order)
            total = 0
            for op in orderproduct:
                amount = op.calcprice()
                total = total + amount
            context['total'] = total
            context['orderproduct'] = orderproduct
            context["count"] = OrderProduct.objects.filter(order = order).count()
        else:
            count = 0
            context["count"] = 0
        context["brands"] = brands
        context["brandcategory"] = brandcategory
        context["products"] = Product.objects.all()
        context["categories"] = Category.objects.all
        return context
class Cart(ListView):
    model = OrderProduct
    template_name = 'cart_page.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        orderr = Order.objects.filter(user = user,complete = False)
        if orderr.exists():
            order = orderr[0]
            orderproduct = OrderProduct.objects.filter(order = order)
            total = 0
            for op in orderproduct:
                amount = op.calcprice()
                total = total + amount
                order.total = total
                order.save()
            context['total'] = total
            context['orderproduct'] = orderproduct
            context["count"] = OrderProduct.objects.filter(order = order).count()
        else:
            context["count"] = 0
        context["categories"] = Category.objects.all
        return context
class Checkout(CreateView,LoginRequiredMixin):
    model = Customer
    form_class = CustomerForm
    template_name = 'checkoutpage.html'
    success_url = reverse_lazy('ecom:successpage')
    def post(self,request):
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.user = request.user
            customer.save()
            order = Order.objects.get(user=request.user,complete=False)
            order.date_ordered = timezone.now()
            order.customer = customer
            order.number_of_items = OrderProduct.objects.filter(order = order).count()
            order.complete = True
            order.save()
            return redirect('ecom:successpage')
        else:
            print("Invalid Form")
            return redirect('ecom:checkout')   
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        orderr = Order.objects.filter(user = self.request.user,complete = False)
        if orderr.exists():
            order = orderr[0]
            context["count"] = OrderProduct.objects.filter(order = order).count()
        else: 
            context["count"] = 0
        context["categories"] = Category.objects.all
        return context
class success(TemplateView):
    template_name = 'successpage.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = 0
        context["categories"] = Category.objects.all
        return context
class Orders(ListView):
    template_name = 'orderspage.html'
    model = Order
    def get_context_data(self,**kwargs):
        orders = Order.objects.filter(user = self.request.user, complete = True)
        context = super().get_context_data(**kwargs)
        if orders.exists():
            context['orders'] = orders
            context['order_count'] = orders.count()
        else:
            context['order_count'] = 0
        context["categories"] = Category.objects.all
        orderr = Order.objects.filter(user = self.request.user,complete = False)
        if orderr.exists():
            order = orderr[0]
            context["count"] = OrderProduct.objects.filter(order = order).count()
        else: 
            context["count"] = 0
        return context
class order_detail(DetailView):
    model = Order
    template_name = 'orderdetail.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        orderr = Order.objects.filter(user = self.request.user, complete = False)
        if orderr.exists():
            order = orderr[0]
            context["count"] = OrderProduct.objects.filter(order = order).count()
        else: 
            context["count"] = 0
        order = Order.objects.get(pk=self.kwargs.get('pk'))
        products = OrderProduct.objects.filter(order = order)
        context["products"] = products
        context["categories"] = Category.objects.all()
        return context


# FUNCTIONALITIES
def addtocart(request,pk):
    product = get_object_or_404(Product, pk=pk)
    brand = product.brand
    category = brand.category
    slug = category.slug
    order_list = Order.objects.filter(user = request.user, complete = False)
    if order_list.exists():
        order = order_list[0]
        orderproduct = OrderProduct.objects.filter(product = product, order = order,size = request.POST["size"])
        if orderproduct.exists():
            orderproduct = OrderProduct.objects.get(order = order,product = product,size = request.POST["size"])
            orderproduct.quantity = orderproduct.quantity + 1
            orderproduct.save()
            return redirect('ecom:products',slug = slug)
        else:
            orderproduct = OrderProduct.objects.create(order = order, product = product)
            orderproduct.size = request.POST["size"]
            orderproduct.save()
            return redirect('ecom:products',slug = slug)
    else:
        order = Order.objects.create(user = request.user)
        orderproduct = OrderProduct.objects.create(order = order,product = product,size = request.POST["size"])
        return redirect('ecom:products',slug = slug)

def addtocart_cart(request,pk,size):
    product = get_object_or_404(Product, pk=pk)
    brand = product.brand
    category = brand.category
    slug = category.slug
    order_list = Order.objects.filter(user = request.user, complete = False)
    if order_list.exists():
        order = order_list[0]
        orderproduct = OrderProduct.objects.filter(product = product, order = order,size = size)
        if orderproduct.exists():
            orderproduct = OrderProduct.objects.get(order = order,product = product,size = size)
            orderproduct.quantity = orderproduct.quantity + 1
            orderproduct.save()
            return redirect('ecom:cart')
        else:
            orderproduct = OrderProduct.objects.create(order = order, product = product,size = size)
            orderproduct.save()
            return redirect('ecom:cart')
    else:
        order = Order.objects.create(user = request.user)
        orderproduct = OrderProduct.objects.create(order = order,product = product,size = size)
        return redirect('ecom:cart')

def removefromcart(request,pk,size):
    product = get_object_or_404(Product,pk=pk)
    order_list = Order.objects.filter(user = request.user, complete = False)
    if order_list.exists():
        order = order_list[0]
        orderproduct = OrderProduct.objects.filter(product = product, order = order,size = size)
        if orderproduct.exists():
            orderproduct = OrderProduct.objects.get(order = order,product = product,size = size)
            if orderproduct.quantity == 1:
                orderproduct.delete()
                return redirect('ecom:cart')
            elif orderproduct.quantity>1:
                orderproduct.quantity = orderproduct.quantity - 1
                orderproduct.save()
                return redirect('ecom:cart')

def deleteitem(request,pk,size):
    product = get_object_or_404(Product,pk=pk)
    order_list = Order.objects.filter(user = request.user, complete = False)
    if order_list.exists():
        order = order_list[0]
        orderproduct = OrderProduct.objects.filter(product = product, order = order,size = size)
        if orderproduct.exists():
            orderproduct = OrderProduct.objects.get(order = order,product = product,size = size)
            orderproduct.delete()
            return redirect('ecom:cart')

        

