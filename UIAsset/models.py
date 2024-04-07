from django.db import models
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# -----------------For product---------------------------------

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="this store category name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255, help_text="this will store sub category name")
    categories = models.ManyToManyField(Category, help_text="manyTOmany field with subcategory")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, help_text="this for tag name")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    type = models.CharField(max_length=100, unique=True,
                            help_text="this will store product type like: single, pack, kit,template")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.type


class AssetType(models.Model):
    type = models.CharField(max_length=255, help_text="this will store Asset type like:jpg,png,mp4 ")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.type

class Image(models.Model):
    url=models.URLField(help_text="for product asset Image URLs")
    is_hero_img=models.BooleanField(default=False)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE,
                                   help_text='This will store file like - jpg, mp4')
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)


class Pack(models.Model):
    title = models.CharField(max_length=255, help_text="this will store product title")
    credits = models.IntegerField(default=0,help_text="this for credits")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text="this for creator of product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="for category of product")
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE,
                                     help_text="for type of product i.e single ,pack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, help_text="for tag name of product")
    no_of_items = models.IntegerField(default=0,help_text="number of items in product")
    is_free = models.BooleanField(default=False,help_text="if product free or paid")
    is_active=models.BooleanField(default=True)
    is_approved=models.BooleanField(default=False)
    base_price=models.IntegerField(default=0,help_text="this for base price")
    discount_price=models.IntegerField(default=0,help_text="this for discount price")
    image= models.ManyToManyField(Image,help_text="for thumbnail images")


    # def save(self, *args, **kwargs):
    #     existing_pack = Pack.objects.filter(title=self.title).first()
    #     if existing_pack:
    #         raise ValidationError('Product with the same title already exists')
    #     super().save(*args, **kwargs)
   
   


    def __str__(self):
        return self.title
    
class AssetTag(models.Model):
    name = models.CharField(max_length=255, help_text="this for tag name")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class AssetFile(models.Model):
    url=models.URLField(help_text="for product asset URLs")
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE,
                                   help_text='This will store file like - jpg, mp4')
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    

    

class Asset(models.Model):
    name = models.CharField(max_length=255, help_text="this for Asset name")
    pack= models.ForeignKey(Pack,on_delete=models.SET_NULL, null=True,
                                help_text="this indicate that asset relate to particular product")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text="this for creator of product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="for category of product")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_free=models.BooleanField(default=False)
    credits=models.IntegerField(default=0,help_text="this for credits")
    is_active=models.BooleanField(default=True)
    tag=models.ManyToManyField(AssetTag, help_text="for tag name of asset")
    asset_file= models.ManyToManyField(AssetFile)
    image= models.ManyToManyField(Image,help_text="for thumbnail images")
   
   

class SavedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             help_text="this refer particular user that saved items")
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE,
                                help_text="this refers particular product that saved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavedSingleAsset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             help_text="this refer particular user that saved items")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,
                              help_text="this refers particular product that saved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PackDownload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             help_text="refer to user that download product")
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, help_text="refer to product that download")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssetDownload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             help_text="refer to user that download product")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, help_text="refer to Asset that download")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SortType(models.Model):
    name = models.CharField(max_length=100, help_text="for type of sort like relevant, popular etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ------------------------------------------------------

# -------------for billing and payment--------------------------

class BillingType(models.Model):
    name = models.CharField(max_length=255, help_text="type of billing i.e renewal etc ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BillingHistory(models.Model):
    billing_type = models.ForeignKey(BillingType, on_delete=models.CASCADE, help_text="refer to billingType table")
    amount = models.FloatField(help_text="for billing amount")
    invoice = models.URLField(help_text="for Invoice PDFs")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer to user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for refer user")
    card_number = models.BigIntegerField(help_text="for card number")
    expiry_date = models.DateField(help_text="for card expiary date")
    security_code = models.CharField(max_length=4, help_text="cvv code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Country(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=56)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=256)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BillingPersonalInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for refer user")
    first_name = models.CharField(max_length=100, help_text="for first name")
    last_name = models.CharField(max_length=100, help_text="for last name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, help_text="for country name")
    address1 = models.TextField(max_length=200, help_text="for address1")
    address2 = models.TextField(blank=True, null=True, help_text="for address2")
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text="for city name")
    state = models.ForeignKey(State, on_delete=models.CASCADE, help_text="for state")
    postal_code = models.IntegerField(help_text="for postal code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionType(models.Model):
    name = models.CharField(max_length=255, help_text="for transaction type i.e sale,purchasse etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PackTransaction(models.Model):
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        help_text="for credit amount of product")
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       help_text="for debit amount record for product")
    tran_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
                                  help_text="refer transaction type i.e purchase ,sale etc.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer particular user")
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, null=True, blank=True,
                                help_text="for refer product", )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscribe(models.Model):
    email=models.EmailField(max_length=254)
    is_subscribe=models.BooleanField()



# -----------------------------------------