from django.urls import path
from .views import signup, store_page
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
	#Leave as empty string for base url

	# path('signup/', views.SignupPage, name="signup"),
	# path('login/', views.LoginPage, name="login"),
	path('signup/', signup, name='signup'),
	path('store/', store_page, name='store_page'),
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/' , views.processOrder, name="process_order"),
]