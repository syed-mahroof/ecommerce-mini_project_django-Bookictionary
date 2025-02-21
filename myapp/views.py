# views.py
from django.shortcuts import render,redirect,get_object_or_404 # type: ignore
from .models import Product,Cart,Register,Order
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from django.http import FileResponse # type: ignore
from io import BytesIO
from reportlab.pdfgen import canvas # type: ignore
from django.http import HttpResponse # type: ignore



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
    if not request.session.get('id'):  # Ensure session contains user ID
        return redirect('login')  # Redirect to login if not authenticated

    product = get_object_or_404(Product, id=product_id)

    # Ensure cart is linked to a user
    user_id = request.session.get('id')  
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        user_id=user_id,  # Make sure each cart item is linked to a specific user
        defaults={"price": product.price, "quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')  # Redirect to cart page after adding item


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
    if request.method == 'POST':    
        email = request.POST.get('email')
        password = request.POST.get('password')
        rg = Register.objects.filter(email=email, password=password)

        if rg.exists():
            user_details = rg.first()
            request.session['id'] = user_details.id
            request.session['name'] = user_details.name
            request.session.modified = True  # Ensure session is updated

            return redirect('products')  # Redirect to products page after login
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')  # Redirect back to login page

    return render(request, 'login.html')

    

def login(request):
    return render(request,'login.html')

def logoutuser(request):
    request.session.flush()  # Clears the session data
    logout(request)
    return redirect('home')  # Redirect to login page after logout



def checkout(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id)
    
    if not cart_items.exists():
        return redirect('cart')

    for item in cart_items:
        Order.objects.create(
            user_id=user_id,
            product=item.product,
            quantity=item.quantity,
            total_price=float(item.product.price) * item.quantity
        )
    
    cart_items.delete()  # Clear the cart after checkout

    return redirect('order_placed')

def order_placed(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    orders = Order.objects.filter(user_id=user_id).order_by('-ordered_at')
    return render(request, "order_placed.html", {"orders": orders})


def purchase_history(request):
    if not request.session.get('id'):
        messages.warning(request, "Login to view purchase history.")
        return redirect("login")

    user_id = request.session.get('id')
    orders = Order.objects.filter(user_id=user_id).order_by("-ordered_at")

    return render(request, "purchase_history.html", {"orders": orders})

def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    user = Register.objects.get(id=order.user_id)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Invoice")
    p.drawString(100, 780, f"Order ID: {order.id}")
    p.drawString(100, 760, f"Customer: {user.name}")
    p.drawString(100, 740, f"Product: {order.product.name}")
    p.drawString(100, 720, f"Quantity: {order.quantity}")
    p.drawString(100, 700, f"Total Price: ₹{order.total_price}")
    p.drawString(100, 680, f"Date: {order.ordered_at.strftime('%Y-%m-%d %H:%M:%S')}")

    p.showPage()
    p.save()

    return response