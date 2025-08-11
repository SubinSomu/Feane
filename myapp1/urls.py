from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='myapp1'
urlpatterns = [
    path('', views.index, name='home'),
    path('add_food', views.add_food, name='add_food'),
    path('food', views.view_food, name='view_food'),
    path('update_food', views.update_food, name='update_food'),
    path('dashboard/delete_food/<int:f_id>/', views.delete_food, name='delete_food'),
    path('view_users/', views.view_users, name='view_users'),
    path('cart/add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('dashboard/add_coupon/', views.add_coupon, name='add_coupon'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
