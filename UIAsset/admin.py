from django.contrib import admin
from .models import *


# Register your models with all fields displayed.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
  

# @admin.register(AssetTag)
# class AssetTagAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at', 'updated_at')

@admin.register(AssetFile)
class AssetFileAdmin(admin.ModelAdmin):
    list_display = ('id','url', 'asset_type')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id','url', 'is_hero_img')


# @admin.register(ProductType)
# class ProductTypeAdmin(admin.ModelAdmin):
#     list_display = ('type', 'created_at', 'updated_at')


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_at', 'updated_at')


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'base_price','discount_price', 'creator', 'category', 'created_at', 'updated_at')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','name','creator', 'base_price','discount_price','category','created_at', 'updated_at')


@admin.register(SavedPack)
class SavedProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'pack', 'created_at', 'updated_at')


@admin.register(PackDownload)
class PackDownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'pack', 'created_at', 'updated_at')


@admin.register(SortType)
class SortTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(BillingType)
class BillingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = ('billing_type', 'amount', 'invoice', 'user', 'created_at', 'updated_at')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'expiry_date', 'security_code', 'created_at', 'updated_at')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at', 'updated_at')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'created_at', 'updated_at')


@admin.register(BillingPersonalInfo)
class BillingPersonalInfoAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'first_name', 'last_name', 'country', 'address1', 'address2', 'city', 'state', 'postal_code', 'created_at',
    'updated_at')


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(PackTransaction)
class PackTransactionAdmin(admin.ModelAdmin):
    list_display = ('credit_amount', 'debit_amount', 'tran_type', 'user', 'pack', 'created_at', 'updated_at')


admin.site.register(SavedAsset)
admin.site.register(Subscribe)