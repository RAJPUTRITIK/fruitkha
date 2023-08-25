from django.urls import path
from seller_app import views
urlpatterns = [

    path('',views.seller_index,name='seller_index'),
    path('seller_register/',views.seller_register,name='seller_register'),
    path('seller_login/',views.seller_login,name='seller_login'),
    path('add_product/',views.add_product,name='add_product'),
    path('seller_logout/',views.seller_logout,name='seller_logout'),
    

]