

from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password, check_password
from .models import MenuItem, Booking, Register, MyUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import *
from myapp1.models import *
def menu_view(request):
    VALID_CATEGORIES = ['burger', 'pizza', 'pasta', 'fries']
    menu_items = MenuItem.objects.all()

    category = request.GET.get('category')
    if category in VALID_CATEGORIES:
        menu_items = menu_items.filter(category=category)

    context = {
        'menu_items': menu_items,
        'categories': VALID_CATEGORIES,
    }
    return render(request, 'menu.html', context)

@require_POST
def add_to_cart(request, item_id):
    try:
        cart = request.session.get('cart', {})
        item_id_str = str(item_id)

        item = MenuItem.objects.get(id=item_id)
        cart[item_id_str] = cart.get(item_id_str, 0) + 1

        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'status': 'success',
            'message': f'Added {item.name} to cart',
            'cart_count': sum(cart.values())
        })
    except MenuItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def book_table(request):
    """
    Handle table booking manually without BookingForm.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        guests = request.POST.get('guests')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not name or not guests or not date or not time:
            messages.error(request, 'All fields are required.')
            return redirect('book')

        try:
            booking = Booking.objects.create(name=name, guests=guests, date=date, time=time)
            booking.save()
            messages.success(request, 'Your table has been booked successfully!')
            return redirect('book')
        except Exception as e:
            messages.error(request, f"Error while booking: {e}")
            return redirect('book')

    return render(request, 'book.html')


class HomeView(TemplateView):
    
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_items'] = FoodItem.objects.all()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        item_ids = [int(k) for k in cart.keys()]
        menu_items = MenuItem.objects.filter(id__in=item_ids)
        item_map = {item.id: item for item in menu_items}

        items = []
        total = 0
        for item_id_str, quantity in cart.items():
            item_id = int(item_id_str)
            item = item_map.get(item_id)
            if item:
                subtotal = item.price * quantity
                items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
                total += subtotal

        context['cart_items'] = items
        context['total'] = total
        return context

class OrderView(TemplateView):
    template_name = 'order.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        phone = request.POST.get('phone', '').strip()

        if not username or not email or not password or not phone:
            messages.error(request, "All fields are required.")
            return redirect('myapp:signup')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('myapp:signup')

        if MyUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('myapp:signup')

        if MyUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('myapp:signup')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect('myapp:signup')

        user = MyUser.objects.create_user(username=username, email=email, password=password, phone=phone)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('myapp:login')

    return render(request, 'signup.html')


def login_html(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        try:
            user = authenticate(request, username=username, password=password)
        except MyUser.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
        else:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('myapp:home')

    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('myapp:home')


def my_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        print(username, password, phone, email)
    return render(request, 'profile.html')
def update_user(request):
    usr=request.user
    if request.method == 'POST':
        fname = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        print(fname,email, phone, address)
        
        usr.username=fname
        usr.email=email
        usr.phone=phone
        usr.address=address
        usr.save()

        
        return redirect('myapp:profile')

def update_password(request):
    if request.method == 'POST':
     
        current_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')


        print(current_password,new_password,confirm_password)
        usr1=request.user
        if not usr1.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('profile')
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect('myapp:update_password')

        usr1.set_password(new_password)
        usr1.save()
        



    return redirect('profile')


def buy_now(request,item_id):
    data=FoodItem.objects.get(id=item_id)
    context={
        'data':data
    }

    return render(request, 'buy_now.html',context)
    





def add_cart(request, p_id, qty):
    usr = request.user
    product = FoodItem.objects.get(id=p_id)
    qty = int(qty)  

   
    existing_cart_item = Cart.objects.filter(user=usr, product=product).first()

    if existing_cart_item:
        
        existing_cart_item.quantity += qty
        existing_cart_item.save()
    else:
       
        Cart.objects.create(user=usr, product=product, quantity=qty)

    return redirect('myapp:show_cart')


def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    cart_data = []
    total = 0

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        cart_data.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    discount = 0
    coupon_code = ""

    if request.method == 'POST':
        C_code = request.POST.get('coupon_code')
        coupon_code = C_code
        try:
            code = Coupon.objects.get(coupon_code=C_code)
            discount = int((code.discount_percent / 100) * total)
            request.session['discount'] = discount
            request.session['coupon_code'] = C_code
            messages.success(request, f"{code.discount_percent}% discount applied!")
        except:
            request.session['discount'] = 0
            request.session['coupon_code'] = ""
            messages.error(request, "Invalid coupon.")

    else:
        discount = request.session.get('discount', 0)
        coupon_code = request.session.get('coupon_code', '')

    final_total = total - discount

    context = {
        'cart_items': cart_data,
        'total': final_total,
        'discount': discount,
        'coupon_code': coupon_code,
        'username': user.username
    }

    return render(request, 'add_cart.html', context)





def delete_cart_item(request, product_id):
    user = request.user
    cart_item =  Cart.objects.filter(user=user, product__id=product_id)
    cart_item.delete()
    return redirect('myapp:show_cart')

def increase_quantity(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product__id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('myapp:show_cart')


def decrease_quantity(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product__id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  
    return redirect('myapp:show_cart')


def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    cart_data = []
    total = 0

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        cart_data.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    discount = request.session.get('discount', 0)
    final_total = total - discount

    context = {
        'user': user,
        'cart_items': cart_data,
        'total': final_total,
        'discount': discount
    }

    return render(request, 'checkout.html', context)






















    
