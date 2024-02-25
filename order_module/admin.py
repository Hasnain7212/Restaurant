from django.contrib import admin

from .models import Category,Quantity,VegNonVeg,MenuItem,UserAdd,CartItem,Cart
# Register your models here.

admin.site.register(Category)
admin.site.register(Quantity)
admin.site.register(VegNonVeg)
admin.site.register(MenuItem)
admin.site.register(UserAdd)
admin.site.register(CartItem)
admin.site.register(Cart)