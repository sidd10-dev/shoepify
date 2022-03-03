from django.urls import path
from . import views
app_name = 'ecom'
urlpatterns = [
    path('category/',views.CategoryPage.as_view(), name = 'category'),
    path('category/<slug:slug>',views.ProductsPage.as_view(), name = 'products'),
    path('addtocart/<int:pk>',views.addtocart, name = 'addtocart'),
    path('addtocartt/<int:pk>/<int:size>',views.addtocart_cart,name = 'addtocart_cart'),
    path('removeitem/<int:pk>/<int:size>',views.removefromcart, name = 'removefromcart'),
    path('deleteitem/<int:pk>/<int:size>',views.deleteitem,name = 'deleteitem'),
    path('cart/',views.Cart.as_view(), name = 'cart'),
    path('checkout/',views.Checkout.as_view(), name = 'checkout'),
    path('successpage/',views.success.as_view(), name = 'successpage'),
    path('orders/',views.Orders.as_view(), name = 'orders'),
    path('orders/<int:pk>',views.order_detail.as_view(), name = 'order_detail'), 
]