from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Quantity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class VegNonVeg(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categorys")
    quantity = models.ManyToManyField(Quantity, related_name="quantitys")
    vegnonveg = models.ForeignKey(VegNonVeg, on_delete=models.CASCADE, related_name="vnv")
    picture = models.ImageField(upload_to='images/', default='settings.MEDIA_ROOT/images/default.jpeg')

    def __str__(self):
        return self.name

class UserAdd(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    userId = models.ForeignKey(UserAdd, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_No = models.IntegerField()

    def __str__(self):
        return f"{self.userId} ({self.item})"

class Cart(models.Model):
    username = models.ForeignKey(UserAdd, on_delete=models.CASCADE, related_name="usernames")
    cart_id = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(CartItem, related_name="cartitems")
    order_status = models.CharField(max_length=20,default='preparing')
    address = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.username} ({self.cart_id})"


