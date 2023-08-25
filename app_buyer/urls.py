
from django.urls import path
from app_buyer import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('otp/', views.otp, name='otp'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('shop/', views.shop, name='shop'),
    path('showcart/', views.showcart, name='showcart'),
    path('search/', views.search, name='search'),
    path('delete_cart/<int:pk>', views.delete_cart, name='delete_cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('single_product/<int:pk>', views.single_product, name='single_product'),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

]
