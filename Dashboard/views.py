from rest_framework.decorators import api_view,permission_classes
from UIAsset.models import Asset, ProductType ,Product,Tag
from django.http import JsonResponse
from Learn.models import *
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_product(request):
    if request.method == 'POST':
        product_data = request.data.get('product')
        try:
            product = Product.objects.create(
                title=product_data['title'],
                #credits=product_data['credits'],
                creator_id=request.user.id,
                category_id=product_data['category'],
                subcategory_id=product_data['subcategory'],
                product_type_id=product_data['product_type'],
                #no_of_items=product_data['no_of_items'],
                #is_free=product_data['is_free'],
            )
            product.tag.set(product_data['tag'])

            return JsonResponse({"message": "Product uploaded successfully", "product_id": product.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)

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
    except Product.DoesNotExist:
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

            product = Product.objects.get(id=product_id)
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

          
            product.no_of_items = total_assets
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
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({"message": "Product deleted successfully"})
    except Product.DoesNotExist:
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

            product = Product.objects.create(
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
