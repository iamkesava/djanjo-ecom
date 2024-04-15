from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Seller(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Product(models.Model):
	STATUS =(
        ('Electronic waste','Electronic waste'),
        ('Furniture waste','Furniture waste'),
        ('Paper waste','Paper waste'),
		)
	name=models.CharField(max_length=40)
	user_id=models.CharField(max_length=40)    
	product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
	price = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()    
	description=models.CharField(max_length=300)
	year = models.CharField(max_length=5,null=True)  
	make = models.CharField(max_length=50,null=True)   
	spec=models.CharField(max_length=100,null=True)    
	cat=models.CharField(max_length=50,null=True,choices=STATUS)
	def get_id(self):
		return self.user.id 
	def __str__(self):
		return self.name



class Stock(models.Model):
	name=models.CharField(max_length=40)
	created_date= models.DateField(null=True)
	quantity = models.PositiveIntegerField()
	date_modified=models.DateField(null=True)
	def __str__(self):
		return self.name

class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    user_id=models.CharField(max_length=20,null=True)   
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
