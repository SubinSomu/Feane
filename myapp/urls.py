from django.urls import path
from . import views
from django.conf import settings
from  django.conf.urls.static import static
app_name='myapp'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('menu.html', views.menu_view, name='menu_html'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('book/', views.book_table, name='book'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('cart/add/<str:item_id>/', views.add_to_cart, name='cart_add'),
    path('login/',views.login_html,name='login'),
    path('signup/',views.signup,name='signup'),
    path('log_out/',views.log_out,name='log_out'),
    path('profile/',views.my_account,name='profile'),
    path('update_user',views.update_user,name='update_user'),
    path('update_password',views.update_password,name='update_password'),
    path('buy/<int:item_id>/', views.buy_now, name='buy_now'),
    path('cart/<int:p_id>/<int:qty>/',views.add_cart,name='cart'),
    path('cartitems/', views.show_cart, name='show_cart'),
    path('delete-cart-item/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('checkout/', views.checkout, name='checkout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.urls import path
# from . import views

# app_name = 'myapp'

# urlpatterns = [
#     path('cartitems/', views.show_cart, name='show_cart'),
#     path('delete-cart-item/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
#     path('increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
#     path('decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
# ]
