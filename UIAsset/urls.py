from django.contrib import admin
from django.urls import path,include
from UIAsset import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('getproduct/<int:category_id>/',views.GetProductDetails),
    path('download-product/',views.download_product),
    path('get-subcategories/<int:category_id>',views.get_subcategories),
    path('get-singleproduct/<int:product_id>/',views.get_singleproduct, name='product_detail'),
    path('related_products/<int:product_id>/',views.related_products),
    path('get-most-downloaded/<int:category_id>/',views.most_downloaded_products),
    path('saved-product/',views.save_for_later),
    path('get-contain-images/<int:product_id>/',views. get_product_contain_images),
    path('get-created-pack-and-asset/',views.creator_data),
    path('related_asset/<int:product_id>/',views.related_asset),
    path('related_product_for_asset/<int:asset_id>/',views.related_product_for_asset),
    path('download-asset/',views.download_single_asset),
    path('saved-asset/',views.save_for_asset),
    path('filter_products/',views.filter_products)

    ]