from django.db import models
from django.conf import settings
from autoslug.fields import AutoSlugField
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# -----------------For product---------------------------------

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="this store category name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='name')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


# class SubCategory(models.Model):
#     name = models.CharField(max_length=255, help_text="this will store sub category name")
#     categories = models.ManyToManyField(Category, help_text="manyTOmany field with subcategory")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
class FileType(models.Model):
    name = models.CharField(unique=True,max_length=255, help_text="this for file type name")
    extension=models.CharField(unique=True,max_length=255, help_text="this for file extension")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    #slug=AutoSlugField(name="name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(unique=True,max_length=255, help_text="this for tag name")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    #slug=AutoSlugField(name="name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


# class ProductType(models.Model):
#     type = models.CharField(max_length=100, unique=True,
#                             help_text="this will store product type like: single, pack, kit,template")
#     updated_at = models.DateField(auto_now=True)
#     created_at = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.type


class AssetType(models.Model):
    name = models.CharField(max_length=255, help_text="this will store Asset type like:jpg,png,mp4 ")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FontType(models.Model):
    name = models.CharField(max_length=255, help_text="this will store font type like:serief,san-serief ")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Image(models.Model):
    url=models.URLField(unique=True,help_text="for product asset Image URLs")
    is_hero=models.BooleanField(default=False,help_text="indicate which image is hero_image from all images")
    # asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE,
                                   #help_text='This will store file like - jpg, mp4')
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_preview=models.BooleanField(default=False,help_text='indicate image is preview image')


    

class AssetFile(models.Model):
    url=models.URLField(unique=True,help_text="for product asset URLs")
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE,
                                   help_text='This will store file like - jpg, mp4')
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    

class Asset(models.Model):
    name = models.CharField(max_length=255,unique=True, help_text="this for Asset name")
    #pack= models.ForeignKey(Pack,on_delete=models.SET_NULL, null=True,
                                #help_text="this indicate that asset relate to particular product")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text="this for creator of product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="for category of product")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_free=models.BooleanField(default=False,help_text="Asset is free or not")
    is_active=models.BooleanField(default=True)
    tags=models.ManyToManyField(Tag, help_text="for tag name of asset")
    asset_file= models.ManyToManyField(AssetFile,help_text="for asset files storage")
    image= models.ManyToManyField(Image,help_text="for thumbnail images")
    base_price=models.IntegerField(default=0,help_text="this for base price")
    discount_price=models.IntegerField(default=0,help_text="this for discount price")
    slug = AutoSlugField(populate_from='name')

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

class Pack(models.Model):
    name= models.CharField(max_length=255, help_text="this will store product title")
    #credits = models.IntegerField(default=0,help_text="this for credits")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text="this for creator of product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="for category of product")
   # product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE,
                                   #  help_text="for type of product i.e single ,pack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, help_text="for tag name of product")
    total_assets = models.IntegerField(default=0,help_text="number of items in product")
    is_free = models.BooleanField(default=False,help_text="if product free or paid")
    is_active=models.BooleanField(default=True)
    is_approved=models.BooleanField(default=False)
    base_price=models.IntegerField(default=0,help_text="this for base price")
    discount_price=models.IntegerField(default=0,help_text="this for discount price")
    image= models.ManyToManyField(Image,help_text="for thumbnail images")
    assets=models.ManyToManyField(Asset,help_text="for all assets file that related to product")
    filetypes=models.ManyToManyField(FileType,help_text="for all filetypes that related to product")
    font_types=models.ManyToManyField(FontType,help_text="for all fonttypes that related to product")
    slug = AutoSlugField(populate_from='name')

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     existing_pack = Pack.objects.filter(title=self.title).first()
    #     if existing_pack:
    #         raise ValidationError('Product with the same title already exists')
    #     super().save(*args, **kwargs)
   
   


    def __str__(self):
        return self.name
    
# class AssetTag(models.Model):
#     name = models.CharField(max_length=255, help_text="this for tag name")
#     updated_at = models.DateField(auto_now=True)
#     created_at = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    

   

class SavedPack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             help_text="this refer particular user that saved items")
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE,
                                help_text="this refers particular product that saved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavedAsset(models.Model):
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
    name = models.CharField(max_length=20,help_text="this for country name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=56,help_text="This for sate name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE,help_text="This refers country")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=256,help_text="This for city name")
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