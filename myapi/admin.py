from django.contrib import admin
from .models import UserModel, Product, Category , CartItem , Cart 

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number')
    search_fields = ('username', 'email')

admin.site.register(UserModel, UserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
from .models import UserModel, Product, Category , CartItem , Cart
from django.contrib import admin


