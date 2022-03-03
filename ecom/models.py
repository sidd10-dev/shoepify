from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255,null = True)
    phone1 = models.CharField(max_length=10,null=True)
    phone2 = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.name
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_pic = models.ImageField(null = True, blank = True)
    slug = models.SlugField(null = True)
    def __str__(self):
        return self.category_name
    def get_absolute_url(self):
        return reverse("ecom:product", kwargs={"slug":self.slug})
class Brand(models.Model):
    brand_name = models.CharField(max_length=50)
    brand_logo = models.ImageField(null = True, blank = True)
    def __str__(self):
        return self.brand_name
class CategoryBrand(models.Model):
    category = models.ForeignKey("ecom.Category",on_delete=models.CASCADE)
    Brand = models.ForeignKey("ecom.Brand", on_delete=models.CASCADE)
    def __str__(self):
        return self.Brand.brand_name + " " +self.category.category_name
class Product(models.Model):
    brand = models.ForeignKey("ecom.CategoryBrand", on_delete=models.CASCADE, default = 1)
    product_name = models.CharField(max_length=50)
    price = models.FloatField()
    product_image = models.ImageField(null = True, blank = True)
    def __str__(self):
        return self.product_name
class Order(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    customer = models.ForeignKey("ecom.Customer", on_delete=models.CASCADE, null=True)
    complete = models.BooleanField(default = False)
    total = models.IntegerField(null = True)
    number_of_items = models.IntegerField(null = True,default = 0)
    date_ordered = models.DateTimeField(null = True)
    def __str__(self):
        return str(self.pk)
class OrderProduct(models.Model):
    order = models.ForeignKey("ecom.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("ecom.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    size = models.IntegerField(null = True,default = 8)
    def __str__(self):
        return str(self.order.pk) + ' ' + self.product.product_name
    def calcprice(self):
        return self.quantity * self.product.price