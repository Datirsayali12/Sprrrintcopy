from django.contrib import admin
from django.urls import path,include
from Dashboard import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
   # path('save-product/<str:product_type>/',views.upload_product),
   
    #path('update-product/<int:product_id>/',views.update_product),
    path('delete-product/<int:product_id>/',views.delete_product),
   
    path('get_tags/',views.get_tag_and_category),
    path('get_all_data/<str:product_type>/',views.get_all_data),
    path('upload-asset/',views.upload_asset),
    #path('upload_pack/',views.upload_pack)
]