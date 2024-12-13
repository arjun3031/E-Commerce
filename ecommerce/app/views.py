from django.shortcuts import render,redirect
from app.models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages



# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def loginpage(request):
    return render(request,'login.html')

def signuppage(request):
    return render(request,'signup.html')

def usercreate(request):
    if request.method=='POST':
        firstname=request.POST['fname']
        lastname=request.POST['lname']
        username=request.POST['uname']
        addresses=request.POST['address']
        mobile=request.POST['phone']
        mail=request.POST['email']
        password=request.POST['pass']
        confirm=request.POST['cpass']
        img=request.FILES.get('img')
        if password==confirm:
            if username == mail:
                messages.info(request, 'Username and email can not be the same')
                return redirect('signuppage')
    
            if User.objects.filter(username=username).exists():
                messages.info(request,'User already exists')
                return redirect('signuppage')
            
            if User.objects.filter(email=mail).exists():
                messages.info(request, 'Email already exists')
                return redirect('signuppage')
            else:
                user=User.objects.create_user(first_name=firstname,last_name=lastname,email=mail,password=password,username=username)
                user.save()
                u=User.objects.get(id=user.id)
                reg=Customer(address=addresses,phone=mobile,image=img,user=u)
                reg.save()
                return redirect('loginpage')
        else:
            messages.info(request,'Password is not matching')
            return redirect('signuppage')
    else:
        return render(request,'signuppage.html')
    
@login_required(login_url='homepage')
def adminhome(request):
    return render(request,'adminhome.html')

def userlog(request):
    if request.method=='POST':
        usname=request.POST['uname']
        passwrd=request.POST['password']
        user=auth.authenticate(username=usname,password=passwrd)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('adminhome')
            else:
                auth.login(request,user)
                return redirect('customerhome')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('loginpage')
    return render(request,'signuppage.html')

@login_required(login_url='homepage')
def categoryadd(request):
    return render(request,'addcategory.html')

def addcategory(request):
    if request.method=='POST':
        catgory=request.POST['cname']
        c=Category(catoegyname=catgory)
        c.save()
        return redirect('categoryadd')
    
@login_required(login_url='homepage')
def managecategory(request):
    c=Category.objects.all()
    return render(request, 'managecategory.html', {'c1':c})

def deletecategory(request, cd):
    ctry=Category.objects.get(id=cd)
    ctry.delete()
    return redirect('managecategory')
    
@login_required(login_url='homepage')
def productadd(request):
    c=Category.objects.all()
    return render(request,'addproduct.html',{'c1':c})

def addproduct(request):
    if request.method=='POST':
        pname=request.POST.get('pname')
        description=request.POST.get('description')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        catgry=request.POST.get('category')
        img=request.FILES.get('img')
        category=Category.objects.get(id=catgry)
        product=Product(productname=pname,description=description,price=price,quantity=quantity,image=img,category=category)
        product.save()
        return redirect('addproduct')  
    categories=Category.objects.all()
    return render(request,'addproduct.html',{'c1':categories})

@login_required(login_url='homepage')
def manageproduct(request):
    p=Product.objects.all()
    return render(request, 'manageproduct.html', {'p1':p}) 

def deleteproduct(request, pd):
    pro=Product.objects.get(id=pd)
    pro.delete()
    return redirect('manageproduct')

@login_required(login_url='homepage')
def managecustomer(request):
    c=Customer.objects.all()
    return render(request, 'managecustomer.html', {'c1':c}) 

def deletecustomer(request, cd):
    cust=Customer.objects.get(id=cd)
    user=cust.user
    if user:
        user.delete
    cust.delete()
    return redirect('managecustomer')

def logout(request):
    auth.logout(request)
    return redirect('homepage')


@login_required(login_url='homepage')
def customerhome(request):
    cust=Customer.objects.get(user=request.user)
    categories=Category.objects.all()  
    product=Product.objects.all()  
    return render(request,'customerhome.html',{'cust1': cust,'c1': categories,'products':product})


def customerprofile(request,cp):
    cust=Customer.objects.get(id=cp)
    return render(request,'customerprofile.html',{'cust1':cust})

def editcustomer(request,ec):
    cust=Customer.objects.get(id=ec)
    user=cust.user

    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        address=request.POST.get('address')
        phone=request.POST.get('phone')

        if User.objects.filter(username=uname).exists() and uname != user.username:
            messages.info(request,'Username already exists')
            return redirect('editcustomer',ec=cust.id)

        if User.objects.filter(email=email).exists() and email != user.email:
            messages.info(request, 'Email already exists')
            return redirect('editcustomer', ec=cust.id)

        user.first_name=fname
        user.last_name=lname
        user.username=uname
        user.email=email
        cust.address=address
        cust.phone=phone

        if 'img' in request.FILES:
            cust.image=request.FILES['img']

        user.save()
        cust.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('customerprofile',cp=cust.id)
    return render(request,'editcustomer.html',{'ct1': user,'cust1': cust})

def itemcard(request, cp):
    category=Category.objects.get(id=cp)  
    products=Product.objects.filter(category=category)  
    return render(request,'itemcard.html',{'category': category,'products':products})

# @login_required
# def cartview(request):
#     customer=Customer.objects.get(user=request.user)
#     cart,created=Cart.objects.get_or_create(customer=customer)
#     cartitems=CartItem.objects.filter(cart=cart)
#     print("Cart Items:",cartitems) 
#     totalitems=sum(item.quantity for item in cartitems)
#     categories=Category.objects.all()
#     return render(request, 'cart.html',{'cartitems': cartitems,'cust1': customer,'c1': categories,'totalitems':totalitems})


# def view_cart(request):
#     cart_items = []
#     item_count = 0

#     if request.user.is_authenticated:
#         try:
#             customer = Customer.objects.get(user=request.user)
#             cart = Cart.objects.get(customer=customer)
#             cart_items = CartItem.objects.filter(cart=cart)
#             item_count = cart_items.count()
#         except (Customer.DoesNotExist, Cart.DoesNotExist):
#             cart_items = []

#     return render(request, 'cart.html', {'cart_items': cart_items, 'cart_item_count': item_count})


# def add_to_cart(request, prod):
#     if request.user.is_authenticated:
#         customer = Customer.objects.get(user=request.user)
#         cart, created = Cart.objects.get_or_create(customer=customer)
#         product = Product.objects.get(id=prod)

#         cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)

#         if not created:
#             cartitem.quantity += 1  
#             cartitem.save() 
#             messages.info(request, f'{product.productname} quantity increased in your cart.')
#         else:
#             messages.success(request, f'{product.productname} has been added to your cart.')

#         return redirect('cart_view')  # Ensure this matches your URL pattern
#     else:
#         messages.error(request, 'You need to log in to add items to your cart')
#         return redirect('loginpage')
# app/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def cartview(request):
    cart_items = []
    total_items = 0
    grand_total = 0

    try:
        # Fetch customer and associated cart
        customer = Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)

        # Fetch cart items
        cart_items = CartItem.objects.filter(cart=cart)
        
        # Calculate total quantity and grand total of cart items
        total_items = sum(item.quantity for item in cart_items)
        grand_total = sum(item.product.price * item.quantity for item in cart_items)
        
    except (Customer.DoesNotExist, Cart.DoesNotExist):
        cart_items = []
        total_items = 0
        grand_total = 0

    # Fetch categories for dropdown or other purposes
    categories = Category.objects.all()

    return render(request, 'cart.html', {
        'cartitems': cart_items,
        'totalitems': total_items,
        'grand_total': grand_total,  # Include grand total
        'c1': categories,
        'cust1': customer,
    })


@login_required
def add_to_cart(request, prod):
    if request.user.is_authenticated:
        customer =Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        product = Product.objects.get(id=prod)
        
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            messages.info(request, f'{product.productname} is already in your cart.')
        else:
            cartitem.quantity += 1
            cartitem.save()
            messages.success(request, f'{product.productname} has been added to your cart.')

        return redirect('cart')
    else:
        messages.error(request, 'You need to log in to add items to your cart.')
        return redirect('loginpage')


def remove_from_cart(request, itm):
    item = CartItem.objects.filter(id=itm).first()
    if item:
        item.delete()
    return redirect('cart')

@login_required
def buyproduct(request, pro):
    product = Product.objects.get(id=pro)
    customer = Customer.objects.get(user=request.user)
    quantity = request.session.get('quantity', 1)  

    if request.method == 'POST':
        if 'increase' in request.POST:
            quantity += 1
        elif 'decrease' in request.POST and quantity > 1:
            quantity -= 1
        request.session['quantity'] = quantity  

    totalprice = product.price * quantity  
    return render(request, 'buyproduct.html', {'product': product, 'customer': customer, 'quantity': quantity, 'total_price': totalprice})

@login_required
def buy_product(request, prdct):
    product = Product.objects.get(id=prdct)
    return redirect('cart')


# def buyproduct(request, pro):
#     product = Product.objects.get(id=pro)
#     customer = Customer.objects.get(user=request.user)
#     quantity = request.session.get('quantity',1)  

#     if request.method=='POST':
#         if 'increase' in request.POST:
#             quantity=quantity+1
#         elif 'decrease' in request.POST and quantity>1:
#             quantity=quantity-1
#         request.session['quantity']=quantity  
#     totalprice=product.price*quantity  
#     return render(request, 'buyproduct.html',{'product':product,'customer':customer,'quantity':quantity,'total_price':totalprice})

# @login_required
# def buy_product(request, prdct):
#     product = Product.objects.get(id=prdct)
#     return redirect('cart_view') 

def about(request):
    return render(request,'about.html')

@login_required(login_url='homepage')
def editproduct(request,ep):
    product=Product.objects.get(id=ep)
    categories=Category.objects.all()

    if request.method=='POST':
        pname=request.POST.get('pname')
        description=request.POST.get('description')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        categoryid=request.POST.get('category')

        if Product.objects.filter(productname=pname).exists() and pname != product.productname:
            messages.info(request,'Product name already exists')
            return redirect('editproduct', ep=product.id)

        product.productname=pname
        product.description=description
        product.price=price
        product.quantity=quantity
        
        if 'img' in request.FILES:
            product.image=request.FILES['img']

        product.category_id=categoryid
        product.save()  

        messages.success(request,'Product updated successfully!')
        return redirect('manageproduct')  
    return render(request,'editproduct.html',{'product':product,'categories':categories})
