from django import forms
from . import models
class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('name','email','address','pincode','phone1','phone2')