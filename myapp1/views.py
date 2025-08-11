
from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem
from .forms import FoodItemForm
from myapp.models import MyUser  
from django.contrib.auth.decorators import login_required
from myapp.models import Cart
from .models import Coupon
from django.contrib import messages





def index(request):
    """Render the index page."""
    return render(request, 'dash/index.html')


def add_food(request):
    """Add a new food item."""
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        print(name, price, image)

        food = FoodItem(name=name, price=price, image=image, description=description)
        food.save()

        return redirect('myapp1:add_food')
    return render(request, 'dash/add_food.html')


def dashboard(request):
    """Render the dashboard with all food items."""
    food_items = FoodItem.objects.all()
    context = {
        'food_items': food_items
    }
    return render(request, 'dashboard/dashboard.html', context)


def view_food(request):
    """View details of a specific food item."""
    item = FoodItem.objects.all()
    
    return render(request, 'dash/views_item.html', {'items': item})

def update_food(request):
    if request.method == 'POST':
        i_id=int(request.POST.get('itemId'))
        new_name=request.POST.get('name')
        new_price=request.POST.get('price')
        new_description=request.POST.get('description')
        new_image=request.FILES.get('image')
        prdt=FoodItem.objects.get(id=i_id)
        prdt.name=new_name
        prdt.description=new_description
        prdt.price=new_price
        print(new_name,new_price,new_description,'okkkkkkkkkkkkkkkkkkkkk')
       


        if new_image:
            prdt.image=new_image
        prdt.save()
        
        return redirect('myapp1:view_food')
def delete_food(request,f_id):
    food=FoodItem.objects.get(id=f_id)
    food.delete()
    return redirect('myapp1:view_food')



def view_users(request):
    users = MyUser.objects.all()
    return render(request, 'dash/view_user.html', {'users': users})




@login_required
def add_cart(request, product_id):
    if request.method == "POST":
        user = request.user
        product = get_object_or_404(FoodItem, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += quantity  
        else:
            cart_item.quantity = quantity   
        cart_item.save()

        return redirect('cart_page')  

    
    return redirect('home')


def add_coupon(request):
    if request.method == 'POST':
        
        code = request.POST.get('coupon_code')
        discount = request.POST.get('discount_percent')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        coupon = Coupon(coupon_code=code,discount_percent=discount,start_date=start,end_date=end)

        coupon.save()

        return redirect('myapp1:add_coupon')  

    return render(request, 'dash/add_coupon.html')

     








     
        


    
        

    


