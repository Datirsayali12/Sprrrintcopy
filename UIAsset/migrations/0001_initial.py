# Generated by Django 5.0.2 on 2024-04-06 17:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='for product asset URLs')),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='this for tag name', max_length=255)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='this will store Asset type like:jpg,png,mp4 ', max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BillingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='type of billing i.e renewal etc ', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='this store category name', max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='this will store product type like: single, pack, kit,template', max_length=100, unique=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SortType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='for type of sort like relevant, popular etc.', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('is_subscribe', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='this for tag name', max_length=255)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='for transaction type i.e sale,purchasse etc.', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='this for Asset name', max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_free', models.BooleanField(default=False)),
                ('credits', models.IntegerField(default=0, help_text='this for credits')),
                ('is_active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(help_text='this for creator of product', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('asset_file', models.ManyToManyField(to='UIAsset.assetfile')),
                ('tag', models.ManyToManyField(help_text='for tag name of asset', to='UIAsset.assettag')),
                ('category', models.ForeignKey(help_text='for category of product', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.category')),
            ],
        ),
        migrations.CreateModel(
            name='AssetDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(help_text='refer to Asset that download', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.asset')),
                ('user', models.ForeignKey(help_text='refer to user that download product', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assetfile',
            name='asset_type',
            field=models.ForeignKey(help_text='This will store file like - jpg, mp4', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.assettype'),
        ),
        migrations.CreateModel(
            name='BillingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(help_text='for billing amount')),
                ('invoice', models.URLField(help_text='for Invoice PDFs')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='refer to user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('billing_type', models.ForeignKey(help_text='refer to billingType table', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.billingtype')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='for product asset Image URLs')),
                ('is_hero_img', models.BooleanField(default=False)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('asset_type', models.ForeignKey(help_text='This will store file like - jpg, mp4', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.assettype')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='image',
            field=models.ManyToManyField(help_text='for thumbnail images', to='UIAsset.image'),
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='this will store product title', max_length=255)),
                ('credits', models.IntegerField(default=0, help_text='this for credits')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('no_of_items', models.IntegerField(default=0, help_text='number of items in product')),
                ('is_free', models.BooleanField(default=False, help_text='if product free or paid')),
                ('is_active', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('base_price', models.IntegerField(default=0, help_text='this for base price')),
                ('discount_price', models.IntegerField(default=0, help_text='this for discount price')),
                ('category', models.ForeignKey(help_text='for category of product', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.category')),
                ('creator', models.ForeignKey(help_text='this for creator of product', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('image', models.ManyToManyField(help_text='for thumbnail images', to='UIAsset.image')),
                ('product_type', models.ForeignKey(help_text='for type of product i.e single ,pack', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.producttype')),
                ('tag', models.ManyToManyField(help_text='for tag name of product', to='UIAsset.tag')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='pack',
            field=models.ForeignKey(help_text='this indicate that asset relate to particular product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='UIAsset.pack'),
        ),
        migrations.CreateModel(
            name='PackDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pack', models.ForeignKey(help_text='refer to product that download', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.pack')),
                ('user', models.ForeignKey(help_text='refer to user that download product', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.BigIntegerField(help_text='for card number')),
                ('expiry_date', models.DateField(help_text='for card expiary date')),
                ('security_code', models.CharField(help_text='cvv code', max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='for refer user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pack', models.ForeignKey(help_text='this refers particular product that saved', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.pack')),
                ('user', models.ForeignKey(help_text='this refer particular user that saved items', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedSingleAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(help_text='this refers particular product that saved', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.asset')),
                ('user', models.ForeignKey(help_text='this refer particular user that saved items', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UIAsset.country')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UIAsset.state')),
            ],
        ),
        migrations.CreateModel(
            name='BillingPersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='for first name', max_length=100)),
                ('last_name', models.CharField(help_text='for last name', max_length=100)),
                ('address1', models.TextField(help_text='for address1', max_length=200)),
                ('address2', models.TextField(blank=True, help_text='for address2', null=True)),
                ('postal_code', models.IntegerField(help_text='for postal code')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(help_text='for refer user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(help_text='for city name', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.city')),
                ('country', models.ForeignKey(help_text='for country name', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.country')),
                ('state', models.ForeignKey(help_text='for state', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.state')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='this will store sub category name', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(help_text='manyTOmany field with subcategory', to='UIAsset.category')),
            ],
        ),
        migrations.CreateModel(
            name='PackTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_amount', models.DecimalField(blank=True, decimal_places=2, help_text='for credit amount of product', max_digits=10, null=True)),
                ('debit_amount', models.DecimalField(blank=True, decimal_places=2, help_text='for debit amount record for product', max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pack', models.ForeignKey(blank=True, help_text='for refer product', null=True, on_delete=django.db.models.deletion.CASCADE, to='UIAsset.pack')),
                ('user', models.ForeignKey(help_text='refer particular user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tran_type', models.ForeignKey(help_text='refer transaction type i.e purchase ,sale etc.', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.transactiontype')),
            ],
        ),
    ]
