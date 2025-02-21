# urls.py
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:pk>/', views.product_view, name='product_view'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='cart_add'),
    path('cart/update/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('signup/',views.Signup,name='signup'),
    path('signin/', views.userlog, name='signin'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_placed, name='order_placed'),
    path('download_invoice/<int:order_id>/',views.download_invoice,name='download_invoice'),

]

