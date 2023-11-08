from django.urls import path
from . import views

urlpatterns =[
    path('',views.store,name="store"),
    path('store/',views.store,name="store"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('contact/',views.contact,name="contact"),
    path('offeritems/',views.offeritems,name="offeritems"),
    path('trending/',views.trending,name="trending"),
    path('futureditems/',views.futureditems,name="futureditems"),
    path('welcome/',views.welcome,name="welcome"),
    path('cart/',views.cart,name="cart"),
    path('login/',views.login,name="login"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order")
    
    
]