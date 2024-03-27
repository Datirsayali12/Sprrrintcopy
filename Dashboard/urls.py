from django.contrib import admin
from django.urls import path,include
from Dashboard import views


urlpatterns=[
    path('save-product/',views.upload_product),
    path('save-asset/<int:product_id>/',views.upload_assets),
    path('update-product/<int:product_id>/',views.update_product),
    path('delete-product/<int:product_id>/',views.delete_product),
    path('upload-product-and-asset/',views. upload_product_and_assets),
    #path('upload-product-and-asset1/',views.upload_product_and_assets1)
]