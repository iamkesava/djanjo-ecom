from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']


class SellerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class SellerForm(forms.ModelForm):
    class Meta:
        model=models.Seller
        fields=['address','mobile','description']

class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['name','price','description','product_image','cat','quantity','user_id','year','spec','make']
        description = forms.CharField( widget=forms.Textarea )
        make = forms.CharField( widget=forms.Textarea )
        spec = forms.CharField( widget=forms.Textarea )
        widgets = {
        'description' : forms.Textarea(attrs={'class':'form-control'},
        ),
        'make' : forms.Textarea(attrs={'class':'form-control'},
        ),
        'spec' : forms.Textarea(attrs={'class':'form-control'},
        )
        }


class StockForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['name','quantity','created_date','date_modified']




#address of shipment
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status','user_id']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
