from rest_framework.decorators import api_view,permission_classes
from UIAsset.models import Asset, ProductType ,Pack,Tag,AssetType,AssetTag,AssetFile,Image
from django.http import JsonResponse
from Learn.models import *
from django.db.models import Sum
from rest_framework.response import Response
from django.db.models.functions import Length
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import *
from django.utils import timezone
from django.forms.models import model_to_dict

# @api_view(['POST'])
# def upload_product(request):
#     if request.method == 'POST':
#         u=User.objects.first()
#         c=Category.objects.first()
#         s=Subcategory.objects.first()
#         pt=ProductType.objects.first()

#         p = Pack()
#         p.title="tag3"
#         p.credits=0
#         p.creator=u
#         p.category=c 
#         p.subcategory=s
#         p.product_type=pt  
#         p.no_of_items=0 
#         p.is_free=False 
#         p.is_active=True
#         p.is_approved=False
#         p.base_price=0
#         p.discount_price=0
#         p.save()
#         tag_instance = Tag.objects.create(name="tag_name")  
#         p.tag.add(tag_instance)
#         p.save()
#         image_instance = Image.objects.first()
#         p.image.add(image_instance)
#         p.save()

#         assettag=AssetTag.objects.create(name="tag1")

#         data={
#             "assets": [
#             {
#                 "name": "Asset 1",
#                 "is_free": False,
#                 "credits": 20,
#                 "is_active": True,
#                 "tags": ["tag1", "tag2"],
#                 "image_urls": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
#             },
#             {
#                 "name": "Asset 2",
#                 "is_free": True,
#                 "credits": 10,
#                 "is_active": True,
#                 "tags": ["tag3", "tag4"],
#                 "image_urls": ["http://example.com/image3.jpg", "http://example.com/image4.jpg"]
#             }
#             ]
#         }

#         assettype=AssetType.objects.first()

#         assets_data=data.get('assets', [])


#         for asset_data in assets_data:
#                 asset = Asset()
#                 asset.name = asset_data['name']
#                 asset.pack = p
#                 asset.creator = u 
#                 asset.is_free = asset_data['is_free']
#                 asset.credits = asset_data['credits']
#                 asset.is_active = asset_data['is_active']
#                 asset.save()

#                 tags_data = asset_data.get('tags', [])
#                 for tag_name in tags_data:
#                     tag, _ = AssetTag.objects.get_or_create(name="tag3")
#                     asset.tag.add(tag)

#                 image_urls = asset_data.get('image_urls', [])
#                 for image_url in image_urls:
#                     image, created = Image.objects.get_or_create(
#                     url="http://example.com/image3.jpg",
#                     is_hero_img=False,  
#                     asset_type=assettype,  
#                     )
#                     asset.image.add(image)

#         return JsonResponse({'msg': 'Product and asset created successfully '}, status=200)   




@api_view(['POST'])
def upload_product(request):
        data = request.data
        u = User.objects.first()
       
           

        pack_data = data.get('pack', {})
        category = Category.objects.get(id=pack_data['category_id'])
        subcategory = Subcategory.objects.get(id=pack_data['subcategory_id'])
        product_type = ProductType.objects.get(id=pack_data['product_type_id'])


        pack = Pack.objects.create(
            title=pack_data['title'],
            creator=u,
            category=category,
            subcategory=subcategory,
            product_type=product_type,
            no_of_items=pack_data['no_of_items'],
            is_free=pack_data['is_free'],
            is_active=pack_data['is_active'],
            is_approved=pack_data['is_approved'],
            base_price=pack_data['base_price'],
            discount_price=pack_data['discount_price']

        )
      

        for tag_id in pack_data.get('tagids', []):
            tag = Tag.objects.create(name=tag_id)
            pack.tag.add(tag)

        # pack.tag.add(tag_instance)
        
       
        images_data = pack_data.get('images', [])
       
        for image_data in images_data:
            asset_type, created = AssetType.objects.get_or_create(type=image_data['asset_type'])
            image= Image.objects.create(
                url=image_data['url'],
                is_hero_img=image_data['is_hero_img'],
                asset_type=asset_type
            )
            pack.image.add(image)
        pack.save()

        assets_data=data.get('assets', [])


        for asset_data in assets_data:
                asset = Asset()
                asset.name = asset_data['name']
                asset.pack = pack
                asset.creator = u 
                asset.is_free = asset_data['is_free']
                asset.credits = asset_data['credits']
                asset.is_active = asset_data['is_active']
                asset.save()

                tags_data = asset_data.get('tags', [])
                for tag_name in tags_data:
                    tag, _ = AssetTag.objects.get_or_create(name=tag_name)
                    asset.tag.add(tag)

                    image_urls = asset_data.get('image_urls', [])
                    for image_data in image_urls:
                        image, created = Image.objects.get_or_create(
                            url=image_data['url'],
                            is_hero_img=image_data['is_hero_img'],
                            asset_type=image_data['asset_type']
                        )
                        asset.image.add(image)

        total_assets = Asset.objects.filter(pack=pack).count()
        total_credits = Asset.objects.filter(pack=pack).aggregate(total_credits=Sum('credits'))['total_credits'] or 0
        pack.is_free = total_credits == 0
        pack.no_of_items = total_assets
        pack.credits = total_credits
        print(total_assets)
        print(total_credits)
        pack.save()

        return JsonResponse({'msg': 'Product and asset created successfully '}, status=200)   


      
        



       
       








@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    try:
        product = Pack.objects.get(id=product_id)

        product_data = request.data.get('product')
        product.title = product_data.get('title', product.title)
        product.credits = product_data.get('credits', product.credits)
        product.category_id = product_data.get('category', product.category_id)
        product.subcategory_id = product_data.get('subcategory', product.subcategory_id)
        product.product_type_id = product_data.get('product_type', product.product_type_id)
        product.no_of_items = product_data.get('no_of_items', product.no_of_items)
        product.is_free = product_data.get('is_free', product.is_free)
        product.save()

        if 'tag' in product_data:
           
            product.tag.clear()
        
            for tag_data in product_data['tag']:
                tag_id = tag_data.get('id')
                tag_name = tag_data.get('name')
                tag, created = Tag.objects.get_or_create(id=tag_id, defaults={'name': tag_name})
                product.tag.add(tag)

        return JsonResponse({"message": "Product updated successfully"})
    except Pack.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_assets(request, product_id):
    if request.method == 'POST':
        try:
            product_id = int(product_id)
            asset_data = request.data.get('assets')

            product = Pack.objects.get(id=product_id)
            is_free = asset_item['credits'] == 0

            for asset_item in asset_data:
                Asset.objects.create(
                    name=asset_item['name'],
                    product=product,
                    asset=asset_item['asset'],
                    asset_type_id=asset_item['asset_type'],
                    creator_id=request.user.id,
                    meta_tag=asset_item['meta_tag'],
                    is_hero_img=asset_item['is_hero_img'],
                    is_free=is_free,
                    credits=asset_item['credits']
                )


            total_assets = Asset.objects.filter(product=product).count()
            total_credits = Asset.objects.filter(product=product).aggregate(total_credits=Sum('credits'))['total_credits'] or 0

          
            product.no_of_items = total_assets# not updated
            product.credits = total_credits
            product.is_free = total_credits == 0
            product.save()

            return JsonResponse({"message": "Assets uploaded successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    try:
        product = Pack.objects.get(id=product_id)
        product.delete()
        return JsonResponse({"message": "Product deleted successfully"})
    except Pack.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_product_and_assets(request):
    if request.method == 'POST':
        try:

            product_data = request.data.get('product')
            asset_data = request.data.get('assets')
            user = request.user

            product = Pack.objects.create(
                title=product_data['title'],
                creator_id=user.id,
                category_id=product_data['category'],
                subcategory_id=product_data['subcategory'],
                product_type_id=product_data['product_type'],
            )
            product.tag.set(product_data['tag'])

            for asset_item in asset_data:
                Asset.objects.create(
                    name=asset_item['name'],
                    product=product,
                    asset=asset_item['asset'],
                    asset_type_id=asset_item['asset_type'],
                    creator_id=user.id,
                    meta_tag=asset_item['meta_tag'],
                    is_hero_img=asset_item['is_hero_img'],
                    is_free=asset_item['credits'] == 0,
                    credits=asset_item['credits']
                )

       
            total_assets = len(asset_data)
            total_credits = sum(asset_item['credits'] for asset_item in asset_data)

  
            product.no_of_items = total_assets
            product.credits = total_credits
            product.is_free = total_credits == 0
            product.save()

    
            return JsonResponse({"message": "Product and assets uploaded successfully", "product_id": product.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



# def create_product(product_data, user):
#     try:
#         category_id = product_data.get('category')
#         subcategory_id = product_data.get('subcategory')
#         product_type_id = product_data.get('product_type')
        
#         if not (Category.objects.filter(id=category_id).exists() and \
#                 Subcategory.objects.filter(id=subcategory_id).exists() and \
#                 ProductType.objects.filter(id=product_type_id).exists()):
#             raise ValueError("Invalid category, subcategory, or product type")

#         product = Product.objects.create(
#             title=product_data['title'],
#             creator_id=user.id,
#             category_id=category_id,
#             subcategory_id=subcategory_id,
#             product_type_id=product_type_id,
#         )
#         product.tag.set(product_data['tag'])
#         return product
#     except IntegrityError as e:
#         raise ValueError("Failed to create product: {}".format(str(e)))

# def create_assets(asset_data, product, user):
#     try:
#         for asset_item in asset_data:
#             asset_type_id = asset_item.get('asset_type')
#             if not AssetType.objects.filter(id=asset_type_id).exists():
#                 raise ValueError("Invalid asset type")

#             Asset.objects.create(
#                 name=asset_item['name'],
#                 product=product,
#                 asset=asset_item['asset'],
#                 asset_type_id=asset_type_id,
#                 creator_id=user.id,
#                 meta_tag=asset_item['meta_tag'],
#                 is_hero_img=asset_item['is_hero_img'],
#                 is_free=asset_item['credits'] == 0,
#                 credits=asset_item['credits']
#             )
#     except IntegrityError as e:
#         raise ValueError("Failed to create asset: {}".format(str(e)))

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_product_and_assets1(request):
#     if request.method == 'POST':
#         try:
#             product_data = request.data.get('product')
#             asset_data = request.data.get('assets')
#             user = request.user

#             # Create product
#             product = create_product(product_data, user)

#             # Create assets associated with the product
#             create_assets(asset_data, product, user)

#             # Update product attributes based on assets
#             total_assets = len(asset_data)
#             total_credits = sum(asset_item['credits'] for asset_item in asset_data)
#             product.no_of_items = total_assets
#             product.credits = total_credits
#             product.is_free = total_credits == 0
#             product.save()

#             return JsonResponse({"message": "Product and assets uploaded successfully", "product_id": product.id})

#         except ValueError as e:
#             return JsonResponse({"error": str(e)}, status=400)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     else:
#         return JsonResponse({"error": "Method not allowed"}, status=405)
