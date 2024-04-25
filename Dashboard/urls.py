from django.contrib import admin
from django.urls import path,include
from Dashboard import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[

    path('delete-pack/',views.delete_product),
    path('delete-asset/',views.delete_asset),
    path('get-tags/',views.get_tag_and_category),
    path('upload-asset/',views.upload_asset),
    path('upload-pack/',views.upload_pack),
    path('get-selected-existing/',views.get_selected_existing),
    path('update-asset/',views.update_asset),
    path('get-all-packs/',views.get_all_packs),
    path('update-pack/',views.update_pack),
    path('get-packs-by-title-and-tag/',views.get_packs_by_title_or_tag),
    path('get-all-assets/',views.get_all_assets),
    path('create-from-existing/',views.create_from_existing),
    path('get-assets-by-title-and-tag/',views.get_assets_by_title_and_tag),
    path('get-all-assets/',views.get_all_assets)
   

]