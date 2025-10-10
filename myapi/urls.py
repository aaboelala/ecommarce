from django.urls import path
from . import views


urlpatterns = [
   path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
   path('product-list/', views.ProductList.as_view(), name='product_list'),
   path('product-detail/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
   path('category-list/',views.CategoryList.as_view(), name='category_list'),
   path('category-detail/<slug:slug>/',views.CategoryDetail.as_view(), name='category_detail'),
   path('update-cart-item/',views.Update_OR_Delete_Cart_Item.as_view(), name='update_cart_item'),
   path('add-rating/',views.AddRatingView.as_view(), name='add_rating'),
   path('update-rating/<int:pk>/',views.UpdateRating.as_view(), name='update_rating'),
   path('delete-rating/<int:pk>/',views.delete_rating, name='delete_rating'),
   path('search/',views.search, name='search'),
   path('add-wishlist/',views.add_wishlist, name='add_wishlist'),
   path('create-checkout/',views.create_checkout_session, name='create_checkout_session'),
   path('user-signup/',views.user_signup, name='user_signup'),
  

]

