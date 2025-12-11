from django.urls import path ,include
from . import views

urlpatterns = [
    path('',views.index,name='account_index'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<str:event_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/update/<int:item_id>/', views.update_tickets, name='update_tickets'),


]
