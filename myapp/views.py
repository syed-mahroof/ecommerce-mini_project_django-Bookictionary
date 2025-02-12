# views.py
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,Register
from django.contrib import messages



# from django.http import HttpResponse

# Create your views here.

# def msg(request):
#     return HttpResponse("Hello, World!")

def home(request):
    return render(request, 'home.html')


def products(request):
      query=request.GET.get('search')
      if query:
          products=Product.objects.filter(name=query)
      else:
          products=Product.objects.all()    
          
      return render(request, 'products.html', {'products':products,'q':query})
      
def product_view(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product_view.html', {'product':product})      


def cart(request):
    cart_items = Cart.objects.all()  # Get all cart items
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)  # Calculate total

    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        product=product,
        defaults={"price": product.price, "quantity": 1}  # Set initial quantity
    )

    if not created:
        cart_item.quantity += 1  # Increment quantity if item already exists
        cart_item.save()

    return redirect('cart')  # Redirect to cart page  

def update_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, product_id=product_id)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart')


def Signup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password==cpassword:
            Register(name=name,email=email,phone=phone,password=password,cpassword=cpassword).save()
    return render(request,'register.html')


def userlog(request):
    if request.method=='POST':    
        email=request.POST.get('email')
        password=request.POST.get('password')
        rg= Register.objects.filter(email=email,password=password)
        if rg:
            user_details=Register.objects.get(email=email,password=password)
            id=user_details.id
            name=user_details.name

            request.session['id']=id           #session is used to logged in upto the logout
            request.session['name']=name
            
            messages.success(request, f'Welcome, {name}!')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid credentials')
            return render(request,'login.html')
    else:
        return render(request,'home.html')
    

def login(request):
    return render(request,'login.html')