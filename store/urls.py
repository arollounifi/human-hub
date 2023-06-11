from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import view_cart, add_to_cart, remove_from_cart, update_cart_item


#TODO add a home page
urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/', update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_complete, name='order_complete'),
    ]

