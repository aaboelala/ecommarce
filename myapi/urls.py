from django.urls import path
from . import views


urlpatterns = [
   path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
   path('product-list/', views.product_list, name='product_list'),
   path('product-detail/<slug:slug>/', views.product_detail, name='product_detail'),
   path('category-list/',views.category_list, name='category_list'),
   path('category-detail/<slug:slug>/',views.category_detail, name='category_detail'),
   path('update-cart-item/',views.update_cart_item, name='update_cart_item'),
   path('deleted-from-cart/<int:pk>/',views.delete_from_cart, name='delete_from_cart'),
   path('add-rating/',views.add_rating, name='add_rating'),
   path('update-rating/<int:pk>/',views.update_rating, name='update_rating'),
   path('delete-rating/<int:pk>/',views.delete_rating, name='delete_rating'),
   path('search/',views.search, name='search'),
   path('add-wishlist',views.add_wishlist, name='add_wishlist'),

]

