from django.contrib import admin
from .models import *
admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
# admin.site.register(PhoneNumber)
admin.site.register(CategoryBrand)
# admin.site.register(BrandProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)
# admin.site.register(Invoice)
# admin.site.register(CustomerProduct)
