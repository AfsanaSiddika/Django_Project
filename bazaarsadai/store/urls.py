from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url

	# path('signup/', views.SignupPage, name="signup"),
	# path('login/', views.LoginPage, name="login"),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_view, name='login'),
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/' , views.processOrder, name="process_order"),
]