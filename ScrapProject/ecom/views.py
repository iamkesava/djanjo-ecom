from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from .models import Stock
from django.utils import timezone
from django.http import FileResponse
from reportlab.pdfgen import canvas
import datetime
from .models import Product

def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'ecom/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'ecom/customersignup.html',context=mydict)


def seller_signup_view(request):
    userForm=forms.SellerUserForm()
    sellerForm=forms.SellerForm()
    mydict={'userForm':userForm,'sellerForm':sellerForm}
    if request.method=='POST':
        userForm=forms.SellerUserForm(request.POST)
        sellerForm=forms.SellerForm(request.POST,request.FILES)
        if userForm.is_valid() and sellerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            seller=sellerForm.save(commit=False)
            seller.user=user
            seller.save()
            my_seller_group = Group.objects.get_or_create(name='SELLER')
            my_seller_group[0].user_set.add(user)
        return HttpResponseRedirect('sellerlogin')
    return render(request,'ecom/sellersignup.html',context=mydict)

#-----------for checking user iscustomer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def is_seller(user):
    return user.groups.filter(name='SELLER').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    elif is_seller(request.user):
        return redirect('seller-products')
    else:
        return redirect('admin-dashboard')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'ecom/admin_dashboard.html',context=mydict)


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'ecom/view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def view_seller_view(request):
    sellers=models.Seller.objects.all()
    return render(request,'ecom/view_seller.html',{'sellers':sellers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


# admin delete seller
@login_required(login_url='adminlogin')
def delete_seller_view(request,pk):
    seller=models.Seller.objects.get(id=pk)
    user=models.User.objects.get(id=seller.user_id)
    user.delete()
    seller.delete()
    return redirect('view-seller')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'ecom/admin_update_customer.html',context=mydict)

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'ecom/admin_products.html',{'products':products})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'ecom/admin_add_products.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'ecom/admin_update_product.html',{'productForm':productForm})
    
    
    
    
    
    
# admin view the stock
@login_required(login_url='adminlogin')
def admin_stocks_view(request):
    stocks=models.Stock.objects.all()
    return render(request,'ecom/admin_stocks.html',{'stocks':stocks})


# admin add stock by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_stock_view(request):
    stockForm=forms.StockForm()
    if request.method=='POST':
        stockForm=forms.StockForm(request.POST, request.FILES)
        if stockForm.is_valid():
            stockForm.save()
        return HttpResponseRedirect('admin-stocks')
    return render(request,'ecom/admin_add_stocks.html',{'stockForm':stockForm})


@login_required(login_url='adminlogin')
def delete_stock_view(request,pk):
    stock=models.Stock.objects.get(id=pk)
    stock.delete()
    return redirect('admin-stocks')


@login_required(login_url='adminlogin')
def update_stock_view(request,pk):
    stock=models.Stock.objects.get(id=pk)
    stockForm=forms.StockForm(instance=stock)
    if request.method=='POST':
        stockForm=forms.StockForm(request.POST,request.FILES,instance=stock)
        if stockForm.is_valid():
            stockForm.save()
            return redirect('admin-stocks')
    return render(request,'ecom/admin_update_stock.html',{'stockForm':stockForm})    
    
    
    
    


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'ecom/admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'ecom/update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'feedbacks':feedbacks})



#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})

def csearch_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(cat__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/ccustomer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})

# any one can add product to cart, no need of signin
def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'ecom/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response



# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                total=total+p.price
    return render(request,'ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response


def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'ecom/send_feedback.html', {'feedbackForm':feedbackForm})


#---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/customer_home.html',{'products':products,'product_count_in_cart':product_count_in_cart})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def ccustomer_home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/ccustomer_home.html',{'products':products,'product_count_in_cart':product_count_in_cart})


# shipment address before placing order
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            email = addressForm.cleaned_data['Email']
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)
                    for p in products:
                        total=total+p.price

            response = render(request, 'ecom/payment.html',{'total':total})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            return response
    return render(request,'ecom/customer_address.html',{'addressForm':addressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})




# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed
@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch product id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
    customer=models.Customer.objects.get(user_id=request.user.id)
    products=None
    email=None
    mobile=None
    address=None
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            # Here we get products list that will be ordered by one customer at a time

    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']

    # here we are placing number of orders as much there is a products
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for product in products:
        models.Orders.objects.get_or_create(customer=customer,product=product,status='Pending',email=email,mobile=mobile,address=address,user_id=product.user_id)

    # after order placed cookies should be deleted
    response = render(request,'ecom/payment_success.html')
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'ecom/my_order.html',{'data':zip(ordered_products,orders)})




#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=models.Orders.objects.get(id=orderID)
    product=models.Product.objects.get(id=productID)
    mydict={
        'orderDate':order.order_date,
        'customerName':request.user,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.product_image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return render_to_pdf('ecom/download_invoice.html',mydict)



@login_required(login_url='sellerlogin')
def download_yearwise_view(request):
    query = request.GET['query']
    products=models.Product.objects.all().filter(year__icontains=query,user_id = request.user.id)
    return render_to_pdf('ecom/download_yearwise.html',{'products':products})


@login_required(login_url='sellerlogin')
def download_catwise_view(request):
    query = request.GET['query']
    products=models.Product.objects.all().filter(cat__icontains=query,user_id = request.user.id)
    return render_to_pdf('ecom/download_catwise.html',{'products':products})


@login_required(login_url='sellerlogin')
def download_namewise_view(request):
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query,user_id = request.user.id)
    return render_to_pdf('ecom/download_namewise.html',{'products':products})


@login_required(login_url='sellerlogin')
def download_datewise_view(request):
    query = request.GET['query']
    stocks=models.Stock.objects.all().filter(date_modified__icontains=query)
    return render_to_pdf('ecom/download_datewise.html',{'stocks':stocks})



@login_required(login_url='sellerlogin')
def ndownload_view(request,pk):
    products=models.Product.objects.all().filter(id=pk)
    return render_to_pdf('ecom/download_namewise.html',{'products':products})


@login_required(login_url='sellerlogin')
def cdownload_view(request,pk):
    products=models.Product.objects.all().filter(id=pk)
    return render_to_pdf('ecom/download_catwise.html',{'products':products})

@login_required(login_url='sellerlogin')
def ydownload_view(request,pk):
    products=models.Product.objects.all().filter(id=pk)
    return render_to_pdf('ecom/download_yearwise.html',{'products':products})

@login_required(login_url='sellerlogin')
def ddownload_view(request,pk):
    stocks=models.Stock.objects.all().filter(id=pk)
    return render_to_pdf('ecom/download_datewise.html',{'stocks':stocks})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'ecom/my_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/edit_profile.html',context=mydict)






@login_required(login_url='sellerlogin')
def seller_dashboard_view(request):
    # for cards on dashboard    
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'ecom/seller_dashboard.html',context=mydict)




@login_required(login_url='sellerlogin')
@user_passes_test(is_seller)
def smy_profile_view(request):
    seller=models.Seller.objects.get(user_id=request.user.id)
    return render(request,'ecom/smy_profile.html',{'seller':seller})


@login_required(login_url='sellerlogin')
@user_passes_test(is_seller)
def sedit_profile_view(request):
    seller=models.Seller.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=seller.user_id)
    userForm=forms.SellerUserForm(instance=user)
    sellerForm=forms.SellerForm(request.FILES,instance=seller)
    mydict={'userForm':userForm,'sellerForm':sellerForm}
    if request.method=='POST':
        userForm=forms.SellerUserForm(request.POST,instance=user)
        sellerForm=forms.SellerForm(request.POST,instance=seller)
        if userForm.is_valid() and sellerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            sellerForm.save()
            return HttpResponseRedirect('smy-profile')
    return render(request,'ecom/sedit_profile.html',context=mydict)



@login_required(login_url='sellerlogin')
@user_passes_test(is_seller)
def seller_home_view(request):
    products=models.Product.objects.all().filter(user_id = request.user.id)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/sseller_products.html',{'products':products})


@login_required(login_url='sellerlogin')
@user_passes_test(is_seller)
def cseller_home_view(request):
    products=models.Product.objects.all().filter(user_id = request.user.id)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/csseller_products.html',{'products':products})


@login_required(login_url='sellerlogin')
def seller_products_view(request):
    products=models.Product.objects.all().filter(user_id = request.user.id)   
    return render(request,'ecom/seller_products.html',{'products':products})

def ssearch_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query,user_id = request.user.id)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/sseller_products.html',{'products':products,'word':word})
    return render(request,'ecom/slogout.html')
    
    
def ysearch_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(year__icontains=query,user_id = request.user.id)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/yseller_products.html',{'products':products,'word':word})
    return render(request,'ecom/slogout.html')    
    

def scsearch_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(cat__icontains=query,user_id = request.user.id)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/csseller_products.html',{'products':products,'word':word})
    return render(request,'ecom/slogout.html')

def dsearch_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    stocks=models.Stock.objects.all().filter(date_modified__icontains=query)
    ab = request.GET['query']

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/dseller_products.html',{'stocks':stocks,'word':word})
    return render(request,'ecom/slogout.html')  

def dgenerate_pdf_file(request):
    from io import BytesIO
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    query = request.GET['query'] 
    # Create a PDF document
    stocks=models.Stock.objects.all().filter(date_modified__icontains=query)
    p.drawString(100, 750, "DATE WISE STOCK REPORT")
    p.drawString(20, 770, "------------------------------------------------------------------------------------------------------------------------------------") 
    y = 730
    p.drawString(20, 730, "------------------------------------------------------------------------------------------------------------------------------------") 
  
    for stock in stocks:
        p.drawString(100, y - 20, f"Product Name: {stock.name}")
        p.drawString(100, y - 40, f"Quantity: {stock.quantity}")
        p.drawString(20, y - 60, f"------------------------------------------------------------------------------------------------------------------------------------")        
        y -= 60
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer





@login_required(login_url='sellerlogin')
def seller_add_product_view(request):
    user_id=models.Seller.objects.get(user_id=request.user.id)
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            nm = productForm.cleaned_data['name']            
            qty = productForm.cleaned_data['quantity']
            reg = Stock(name=nm, quantity=qty, created_date=timezone.now(),date_modified=timezone.now())          
            reg.save()              
            productForm.save()
        return HttpResponseRedirect('seller-products')
    return render(request,'ecom/seller_add_products.html',{'productForm':productForm})


@login_required(login_url='sellerlogin')
def sdelete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('seller-products')


@login_required(login_url='sellerlogin')
def supdate_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
        
            nm = productForm.cleaned_data['name']            
            qty = productForm.cleaned_data['quantity']
            stock=models.Stock.objects.filter(name=nm).update(quantity=qty,date_modified=timezone.now())
            productForm.save()         
            return redirect('seller-products')
    return render(request,'ecom/seller_update_product.html',{'productForm':productForm})
    
    
    
    
   
@login_required(login_url='sellerlogin')
def seller_stocks_view(request):
    stocks=models.Stock.objects.all()
    return render(request,'ecom/seller_stocks.html',{'stocks':stocks})


# admin add stock by clicking on floating button
@login_required(login_url='sellerlogin')
def seller_add_stock_view(request):
    stockForm=forms.StockForm()
    if request.method=='POST':
        stockForm=forms.StockForm(request.POST, request.FILES)
        if stockForm.is_valid():
            stockForm.save()
        return HttpResponseRedirect('seller-stocks')
    return render(request,'ecom/seller_add_stocks.html',{'stockForm':stockForm})


@login_required(login_url='sellerlogin')
def sdelete_stock_view(request,pk):
    stock=models.Stock.objects.get(id=pk)
    stock.delete()
    return redirect('seller-stocks')


@login_required(login_url='sellerlogin')
def supdate_stock_view(request,pk):
    stock=models.Stock.objects.get(id=pk)
    stockForm=forms.StockForm(instance=stock)
    if request.method=='POST':
        stockForm=forms.StockForm(request.POST,request.FILES,instance=stock)
        if stockForm.is_valid():
            stockForm.save()
            return redirect('seller-stocks')
    return render(request,'ecom/seller_update_stock.html',{'stockForm':stockForm})    
    
    
    
    


@login_required(login_url='sellerlogin')
def seller_view_booking_view(request):
    orders=models.Orders.objects.all().filter(user_id = request.user.id)
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'ecom/seller_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})



@login_required(login_url='sellerlogin')
def sdelete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('seller-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='sellerlogin')
def supdate_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('seller-view-booking')
    return render(request,'ecom/supdate_order.html',{'orderForm':orderForm})


def logout_view(request):
    return render(request,'ecom/logout.html')







#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'ecom/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'ecom/contactussuccess.html')
    return render(request, 'ecom/contactus.html', {'form':sub})




def info_page(request, product_id):
    product = Product.objects.get(id=product_id)
   # return render(request, 'templates/info.html', {'product': product})
    return render(request, 'info.html', {'product': product})
