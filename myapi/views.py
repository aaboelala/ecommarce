import stripe
from django.shortcuts import get_object_or_404
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from django.conf import settings

from .models import Cart,CartItem, Order, OrderItem, Product, Category, Rating, UserModel, Wishlist
from rest_framework import status
from .serializers import CartItemSerializer, ProductListSerializer, ProductDetailSerializer, CategoryListSerializer, CategoryDetailSerializer, CartSerializer, RatingSerializer, UserSerializer
from rest_framework import status
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics , mixins , permissions



stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.WEBHOOK_SECRET #لسة لما ندبلوي ونحط الديبلوي كديستناشن ع سترايب عشان يبعت عليه 

# Create your views here.
class ProductList(generics.ListCreateAPIView):
    queryset =Product.objects.all()
    serializer_class=ProductListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddToCartView(generics.GenericAPIView):
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")

        if not cart_code or not product_id:
            return Response({"detail": "cart_code and product_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # 1️⃣ Get or create the cart
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)

        # 2️⃣ Get product
        product = get_object_or_404(Product, id=product_id)

        # 3️⃣ Check if product already in cart
        cart_item_exists = CartItem.objects.filter(cart=cart, product=product).exists()
        if cart_item_exists:
            return Response(
                {"detail": "This product is already in your cart."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Otherwise, add it
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        # 5️⃣ Return updated cart data
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




# @api_view(['PUT'])
# def update_cart_item(request):
#     cartitem_id=request.data.get("item_id")
#     quantity=request.data.get("quantity")
#     quantity=int(quantity)

#     cartitem=CartItem.objects.get(id=cartitem_id)
#     if quantity > 0:
#         cartitem.quantity=quantity
#         cartitem.save()
#         serializer=CartSerializer(cartitem.cart)
#         return Response(serializer.data)
#     else:
#         cartitem.delete()
#         return Response({"detail":"Item removed from cart"},status=status.HTTP_204_NO_CONTENT)

class Update_OR_Delete_Cart_Item(generics.GenericAPIView):
    serializer_class=CartItemSerializer
    def put(self,request,pk):
        cartitem=get_object_or_404(CartItem,pk=pk)
        quentity=request.data.get('quantity')
        quentity=int(quentity)
        if quentity < 1 :
           return Response({"error":"at least 1"})
        
        cartitem.quantity=quentity
        cartitem.save()
        serializer=self.serializer_class(cartitem)
        return Response(serializer.data)

    def delete(self,request,pk):
        cartitem=get_object_or_404(CartItem,id=pk)
        cartitem.delete()
        return Response({"deleted susscessfully":"you're deletedthe product susscesfully"})


# @api_view(['POST'])
# def add_rating(request):
#     email=request.data.get("email")
#     product_id=request.data.get("product_id")
#     rating=request.data.get("score")
#     review=request.data.get("review")
#     product=Product.objects.get(id=product_id)
#     user= UserModel.objects.get(email=email)
#     if Rating.objects.filter(product=product,user=user).exists():
#         return Response({"error": "you already have a rating"}, status=status.HTTP_400_BAD_REQUEST)
    
#     Rating.objects.create(user=user,product=product,score=rating,review=review)
#     return Response({"success":"rating added successfully"}, status=status.HTTP_201_CREATED)
class AddRatingView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        score = request.data.get("score")
        review = request.data.get("review")
        product = get_object_or_404(Product, id=product_id)

        if Rating.objects.filter(product=product, user=user).exists():
            return Response({"error": "You have already rated this product."}, status=status.HTTP_400_BAD_REQUEST)

        Rating.objects.create(user=user, product=product, score=score, review=review)
        return Response({"success": "Rating added successfully."}, status=status.HTTP_201_CREATED)
    

    
# @api_view(['PUT'])
# def update_rating(request,pk):
#     rating=Rating.objects.get(id=pk)
#     review=request.data.get("score")
#     review_txt=request.data.get("review")
#     if rating:
#         rating.score=review
#     if review:
#         rating.review=review_txt
#     review.save()
#     return Response({"success":"rating updated successfully"}, status=status.HTTP_200_OK)
class UpdateRating(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def put(self,request,pk):
        score=request.data.get('score')
        review=request.data.get('review')
        user=request.user
        rating=get_object_or_404(Rating,id=pk)
        if rating.user != user :
            return Response({"error":"there is error , you can not edit rating of another users "}, status=status.HTTP_409_CONFLICT)
        if score > '5' :
             return Response({"error":"there is error , you can not rate upper of 5 "}, status=status.HTTP_409_CONFLICT)
        rating.score=score
        rating.review=review
        rating.save()
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


@api_view(['POST'])
def create_checkout_session(request):
    cart_code = request.data.get("cart_code")
    email = request.data.get("email")
    cart = Cart.objects.get(cart_code=cart_code)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email= email,
            payment_method_types=['card'],


            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.product.name},
                        'unit_amount': int(item.product.price * 100),  # Amount in cents
                    },
                    'quantity': item.quantity,
                }
                for item in cart.items.all()
            ] + [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'VAT Fee'},
                        'unit_amount': 500,  # $5 in cents
                    },
                    'quantity': 1,
                }
            ],


           
            mode='payment',
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            metadata = {"cart_code": cart_code}
        )
        return Response({'data': checkout_session})
    except Exception as e:
        return Response({'error': str(e)}, status=400)




@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    session = event['data']['object']
    cart_code = session.get("metadata", {}).get("cart_code")

    fulfill_checkout(session, cart_code)


  return HttpResponse(status=200)



def fulfill_checkout(session, cart_code):
    
    order = Order.objects.create(stripe_checkout_id=session["id"],
        amount=session["amount_total"],
        currency=session["currency"],
        customer_email=session["customer_email"],
        status="Paid")
    

    print(session)


    cart = Cart.objects.get(cart_code=cart_code)
    cartitems = cart.cartitems.all()

    for item in cartitems:
        orderitem = OrderItem.objects.create(order=order, product=item.product, 
                                             quantity=item.quantity)
    
    cart.delete()


@api_view(['POST'])
def user_signup(request):
    serializers=UserSerializer(data=request.data)
    if serializers.is_valid():
         serializers.save()
         return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



































    





    







