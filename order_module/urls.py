from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse

from . import views

urlpatterns = [
    path('',views.register, name="register"),
    path("", views.menu, name="menu"),
    path("getitems/<str:category>/", views.get_menu_items, name="getItems"),
    path("save/", views.savecart, name="saveCart"),
    #order status
    path("status/<str:userId>/", views.orderstatus, name="orderstatus")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

