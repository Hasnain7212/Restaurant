from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import uuid
import json
from django.urls import reverse



from .models import MenuItem, Category, Cart, CartItem, UserAdd, VegNonVeg, Quantity

# Create your views here.

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if UserAdd.objects.filter(phone=phone).exists():
            return render(request, 'order_module/register.html', {'error_message': 'User with this phone number already exists.'})

        user = UserAdd(name=name, phone=phone, password=password)
        user.save()

        return render(request, 'order_module/login.html', {'phone': phone})  
    
    return render(request, 'order_module/register.html')
    
def login(request):
    if request.method == 'POST':
        phones = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            usercheck = UserAdd.objects.get(phone=phones, password=password)
            return menu(request, phones)
        except UserAdd.DoesNotExist:
            error_message = 'Invalid phone number or password. Please try again.'
            return render(request, 'order_module/login.html', {'error_message': error_message})

    return render(request, 'order_module/login.html')

def menu(request, userIdNo):
    return render(request, "order_module/menu.html",{
        "userId": userIdNo
    })

def get_menu_items(request,category):
    menu_items = MenuItem.objects.filter(category=(Category.objects.get(name=category)))
    data = [
        {
            'name': item.name,
            'description': item.description,
            'price': str(item.price),
            'category': item.category.name,
            'quantities': [quantity.name for quantity in item.quantity.all()],
            'vegnonveg': item.vegnonveg.name,
            'image': item.picture.url

        }
        for item in menu_items
    ]
    return JsonResponse({'menu_items': data})


def savecart(request):
    if request.method == 'POST':
        userPhone = request.POST.get('userPhone')
        cart_items_json = request.POST.get('cart_item')
        cart_items = json.loads(cart_items_json)
        addressUser = request.POST.get('address')

        try:
            user = UserAdd.objects.get(phone=userPhone)
        except UserAdd.DoesNotExist:
            return JsonResponse({'message': 'User does not exist', 'userPhone': userPhone})

        try:
            cart = Cart.objects.get(username=user)
        except Cart.DoesNotExist:
            cart_id = str(uuid.uuid4())
            cart = Cart.objects.create(username=user, cart_id=cart_id, address=addressUser)

        items_in_cart = []
        for item_data in cart_items:
            item_name = item_data['name']
            description = item_data['description']
            price = item_data['price']
            quantitytype = item_data['quantitytype']
            category = item_data['category']
            vegnonveg = item_data['vegnonveg']
            quantitys = item_data['quantity']

            
            items_in_cart.append(item_data)
            
            
            try:
                category = Category.objects.get(name=category) 
                vegnonveg = VegNonVeg.objects.get(name=vegnonveg)
                quantitytype = Quantity.objects.get(name=quantitytype)

                item, created = MenuItem.objects.get_or_create(
                    name=item_name,
                    description=description,
                    price=price,
                    quantity=quantitytype,
                    category=category,
                    vegnonveg=vegnonveg,
                    defaults={'quantity_No': quantitys}
                )

                if not created:
                    item.quantity_No = quantitys
                    item.save()

                cart_item, cart_item_created = CartItem.objects.get_or_create(
                    userId=user,
                    item=item,
                    quantity_No=quantitys
                )

                cart.items.add(cart_item)
            except MenuItem.DoesNotExist:
                print(f"Item not found: {item_name}, {price}, {category}, {vegnonveg}")
            except Category.DoesNotExist:
                print(f"Category not found: {category}")
            except VegNonVeg.DoesNotExist:
                print(f"VegNonVeg not found: {vegnonveg}")


            orderstatus_url = reverse('orderstatus', kwargs={'userId': userPhone})
            return HttpResponseRedirect(orderstatus_url)


    return render(request, 'order_module/cart.html')


        
        

def orderstatus(request, userId):
    try:
        user = UserAdd.objects.get(phone=userId)
        cart = Cart.objects.get(username=user)
        cart_items = cart.items.all()
        status = cart.order_status
        address = cart.address
        # Calculate total amount
        total_amount = sum(cart_item.item.price * cart_item.quantity_No for cart_item in cart_items)

        # Retrieve related data from CartItem including quantity_No
        cart_item_data = []
        for cart_item in cart_items:
            item_data = {
                'item_name': cart_item.item.name,
                'item_description': cart_item.item.description,
                'item_price': cart_item.item.price,
                'quantity_No': cart_item.quantity_No,
                'total': cart_item.item.price * cart_item.quantity_No ,
            }
            cart_item_data.append(item_data)

    except UserAdd.DoesNotExist:
        user = None
        cart_items = []
        total_amount = 0

    return render(request, 'order_module/cart.html',
                   {'user': user, 'cart_items': cart_items,
                    'item_data': cart_item_data, 'total_amount': total_amount,
                    'status': status, 'address': address})
