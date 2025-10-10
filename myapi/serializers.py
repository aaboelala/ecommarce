
from .models import ProductRating, Rating, UserModel, Product, Category , CartItem , Cart
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True , 'min_length': 8 },
            'first_name': {'required': True},
            
            'last_name': {'required': True},
            'email': {'required': True},
            'username': {'required': True, 'validators': []},  # Disable unique validator
        }


    def create(self, validated_data):
        user=UserModel.objects.create_user(**validated_data)
        return user



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'price']



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']



class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'products']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items','total_price']
    
    def get_total_price(self, obj):
        return obj.total_price()
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'score', 'review', 'created_at']
        
class ProductRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRating
        fields = ["id", "average_rating", "total_reviews"]

class ProductDetailSerializer(serializers.ModelSerializer):
    ratings=RatingSerializer(read_only=True,many=True)
    product_rating=ProductRatingSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'image', 'price','ratings','product_rating']



    

    


    

    

    






