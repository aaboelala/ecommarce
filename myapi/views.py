from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from .models import Cart,CartItem, Product, Category, Rating, UserModel, Wishlist
from rest_framework import status
from .serializers import ProductListSerializer, ProductDetailSerializer, CategoryListSerializer, CategoryDetailSerializer, CartSerializer
from rest_framework import status
from django.db.models import Q

# Create your views here.
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    serializer = CategoryDetailSerializer(category)

    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):

    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")
    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = get_object_or_404(Product, id=product_id)

    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1 
    cartitem.save() 

    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['PUT'])
def update_cart_item(request):
    cartitem_id=request.data.get("item_id")
    quantity=request.data.get("quantity")
    quantity=int(quantity)

    cartitem=CartItem.objects.get(id=cartitem_id)
    if quantity > 0:
        cartitem.quantity=quantity
        cartitem.save()
        serializer=CartSerializer(cartitem.cart)
        return Response(serializer.data)
    else:
        cartitem.delete()
        return Response({"detail":"Item removed from cart"},status=status.HTTP_204_NO_CONTENT)
    
@api_view(['DELETE'])
def delete_from_cart(request,pk):
    cartitem=CartItem.objects.get(id=pk)
    cartitem.delete()
    Response({"deleted susscessfully":"you're deletedthe product susscesfully"})

  
@api_view(['POST'])
def add_rating(request):
    email=request.data.get("email")
    product_id=request.data.get("product_id")
    rating=request.data.get("score")
    review=request.data.get("review")
    product=Product.objects.get(id=product_id)
    user= UserModel.objects.get(email=email)
    if Rating.objects.filter(product=product,user=user).exists():
        return Response({"error": "you already have a rating"}, status=status.HTTP_400_BAD_REQUEST)
    
    Rating.objects.create(user=user,product=product,score=rating,review=review)
    return Response({"success":"rating added successfully"}, status=status.HTTP_201_CREATED)
@api_view(['PUT'])
def update_rating(request,pk):
    rating=Rating.objects.get(id=pk)
    review=request.data.get("score")
    review_txt=request.data.get("review")
    if rating:
        rating.score=review
    if review:
        rating.review=review_txt
    review.save()
    return Response({"success":"rating updated successfully"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])

def delete_rating(request,pk):
    rating=Rating.objects.get(id=pk)
    rating.delete()
    return Response({"susscess":"you're rating is deleted susscessfully"},status=200)


@api_view(['POST'])
def add_wishlist(request,pk):
    gmail=request.data.get("gmail")
    product_id=request.data.get("product_id")
    product=Product.objects.get(id=product_id)
    user=UserModel.objects.get(gmail=gmail)
    wishlist=Wishlist.objects.filter(product=product,user=user)
    if wishlist :
        wishlist.delete()
        return Response ({"susscess":"you're deleted from wishlist"})
    Wishlist.objects.create(user=user,product=product)
    Response({"susscess":"you're added to wishlist"})




@api_view(['GET'])
def search(request):
    query=request.query_params.get('query')
    if not query :
        return Response({"error":"there is no query , try again"},status=200)
    
    products=Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) |
        Q(category__name__icontains=query)
    )

    if not products.exists():
        return Response({"empty result":"there is no product like you search"},status=202)

    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data, status=200)





























    





    







