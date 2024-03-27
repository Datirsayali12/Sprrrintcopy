from django.contrib import admin
from .models import *


# Register your models with all fields displayed.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'created_at', 'updated_at')


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'credits', 'creator', 'category', 'product_type', 'created_at', 'updated_at')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('product', 'asset', 'asset_type', 'meta_tag', 'created_at', 'updated_at')


@admin.register(SavedProduct)
class SavedProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at', 'updated_at')


@admin.register(ProductDownload)
class ProductDownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at', 'updated_at')


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


@admin.register(ProductTransaction)
class ProductTransactionAdmin(admin.ModelAdmin):
    list_display = ('credit_amount', 'debit_amount', 'tran_type', 'user', 'product', 'created_at', 'updated_at')


admin.site.register(SavedSingleAsset)
admin.site.register(Subscribe)