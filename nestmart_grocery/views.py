from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from service.models import Navbar_item,Trending,ContactUs,Product,Category,About_provide,Profile,Cart,Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
def Navbar():
    return Navbar_item.objects.all()
def Products():
    return Product.objects.all()

def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'shop_page.html', {'products': products})


def Category_List():
    return Category.objects.all()
def About_pro():
    return About_provide.objects.all()
def Trending():
    rows=Trending()
    return rows
    
def home(request):
    Row_1 =Product.objects.filter(which_trend__title="Recently").order_by('-id')[:3]
    Row_2 =  Product.objects.filter(which_trend__title="Trending").order_by('-id')[:3]
    Row_3 = Product.objects.filter(which_trend__title="Top rated").order_by('-id')[:3]
    if request.method == 'POST':
        email=request.POST['email']
        subject = "Subcribe- Nestmart"
        message = f"""
        Hello {email},

        Thank you for subscribing! 🎉

        We will notify you on our latest products.

        Best regards,  
        Nestmart Grocery Team
         """
    
        recipient_email = email

        # Send email
        send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [recipient_email])

    data={
        'Navbar':Navbar,
        'Products':Products,
        'Category':Category_List,
        'Recen':Row_1,
        'Trend':Row_2,
        'Top':Row_3,
    }
    return render(request,'index.html',data)   
def aboutUs(request):
    data={
        'Navbar':Navbar,
        'About':About_pro,
        'Products':Products,
        
    }
    return render(request,'about.html',data)
def shop(request):
    data={
        'Navbar':Navbar,
        'Products':Products,
        
    }
    return render(request,'shop_page.html',data)
def contactUs(request):
    data={
        'Navbar':Navbar,
        'Products':Products,
        
    }
    return render(request,'contactus.html',data)


def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password1 = request.POST['password1']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        image = request.FILES.get('image')

        if password != password1:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists!")
            user = User.objects.create_user(username,email,password)
            
            user.first_name = full_name
            user.save()

            profile = Profile(user=user, phone=phone, dob=dob, gender=gender, address=address, image=image)
            profile.save()

            return redirect("login")

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # ma=messages.success(request, 'Logged in successfully!')
            return redirect('home')  # Redirect to a homepage or dashboard
        else:
            messages.error(request, 'Invalid email or password.')
    data={
        'Navbar':Navbar,
        'Products':Products,
        
    }
    return render(request, 'login.html',data)


def contact_us(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = "Contact Us- Nestmart"
        message = f"""
        Hello {full_name},

        Thank you for contacting us! 🎉
        your message:{message}

        Best regards,  
        Nestmart Grocery Team
        """
    
        recipient_email = email

        # Send email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
        # Save to database
        ContactUs.objects.create(full_name=full_name, email=email, message=message)

        # Show success message
        messages.success(request, "Your message has been sent successfully!")
    data={
        'Navbar':Navbar,
        'Products':Products,
        
            }
    return render(request, "contactus.html",data)

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    discount_percentage = 0
    if product.pdiscpri and product.pprice > 0:
        discount_percentage = round((1 - (product.pdiscpri / product.pprice)) * 100)
    data={
        'Navbar':Navbar,
        'product':product,
        'discount_percentage': discount_percentage,
    }
   

    return render(request, "product_page.html",data)

def cate_shop(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product = Product.objects.filter(cate=category)
     
    price_range = request.GET.get('priceRange', 'all')

    if price_range != 'all':
        if price_range == '0-50':
            product = product.filter(pdiscpri__gte=0, pdiscpri__lte=50)
        elif price_range == '51-100':
            product = product.filter(pdiscpri__gte=51, pdiscpri__lte=100)
        elif price_range == '101-200':
            product = product.filter(pdiscpri__gte=101, pdiscpri__lte=200)
        elif price_range == '201-500':
            product = product.filter(pdiscpri__gte=201, pdiscpri__lte=500)
        elif price_range == '500+':
            product = product.filter(pdiscpri__gte=500)
    
    data={
        'Navbar':Navbar,
        'product':product,
        'selected_price': price_range,
        'Products':Products,
        
    }
   

    return render(request, "cate_page.html",data)
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
 
    return redirect('cart_view')

@login_required(login_url='/login/')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)  # Ensure total price is calculated
    data={
        'Navbar':Navbar,
        'cart_items':cart_items,
        'total_price':total_price,
    }
    return render(request, 'cart.html',data)

@login_required(login_url='/login/')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required(login_url='/login/')
def update_cart(request, cart_id, action):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if action == "increase":
        if cart_item.quantity < cart_item.product.pqt:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, "Not enough stock available.")

    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove from cart if quantity reaches 0

    return redirect('cart_view')


@login_required(login_url='/login/')
def checkout(request, product_id=None):
    if product_id:  # Buy Now - Single Product Checkout
        product = get_object_or_404(Product, id=product_id)
        return render(request, "checkout.html", {"single_product": product})

    # Default: Cart-based checkout
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.pdiscpri * item.quantity for item in cart_items)
    data={
        'Navbar':Navbar,"cart_items": cart_items, "total_price": total_price,
    }
    return render(request, "checkout.html",data)

@login_required(login_url='/login/')
def process_checkout(request):
   
    if request.method == "POST":
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")
        
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect("cart_view")

        total_price = sum(item.product.pdiscpri * item.quantity for item in cart_items)

        # Fetch user instance explicitly
        user_instance = User.objects.get(id=request.user.id)

        # Create Order
        order = Order.objects.create(
            user=user_instance,  # Use the fetched user instance
            address=address,
            payment_method=payment_method,
            total_price=total_price
        )

        # Move cart items to OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.pdiscpri
            )

        # Clear Cart
        cart_items.delete()
    
        messages.success(request, "Your order has been placed successfully!")
        return redirect("order_confirmation", order_id=order.id)
    data={
        'Navbar':Navbar,
    }
    return redirect(request,"cart_view",data)

@login_required(login_url='/login/')
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    full_name = request.user.get_full_name() or request.user.username 
   # Email Subject & Message
    subject = "Your Order Confirmation - Nestmart"
    message = f"""
    Hello {full_name},

    Thank you for your order! 🎉

    Order ID: #{order.id}
    Shipping Address: {order.address}
    Payment Method: {order.payment_method}

    We will notify you once your order is shipped.

    Best regards,  
    Nestmart Grocery Team
    """
    
    recipient_email = request.user.email

    # Send email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

    data={
        'Navbar':Navbar,
        'order': order,
    }
    return render(request, "order_confirmation.html",data)

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(pname__icontains=query)[:5]  # Fetch top 5 results
    
    data = [
        {"name": product.pname, "image": product.pimg.url, "price": product.pdiscpri,"id":product.id,}
        for product in products
    ]
    
    return JsonResponse(data, safe=False)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    data={
        'Navbar':Navbar,
        'orders': orders,
    }
    return render(request, 'order_history.html',data)