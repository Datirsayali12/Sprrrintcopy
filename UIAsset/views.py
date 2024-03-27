from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Learn.models import Video, Ebook, Course
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProductDetails(request, category_id):
    if request.method == "GET":
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category_name = category.name.lower()

        if category_name == "video":
            videos = Video.objects.filter(category=category)
            serialized_data = []
            for video in videos:
                serialized_product = {
                    "title": video.title,
                    "overview": video.overview,
                    "creator": video.creator.id,
                    "category": video.category.id,
                    "created_at": video.created_at,
                    "updated_at": video.updated_at,
                }
                serialized_data.append(serialized_product)
            return Response(serialized_data, status=status.HTTP_200_OK)

        elif category_name == "course":
            courses = Course.objects.filter(category=category)
            serialized_data = []
            for course in courses:
                serialized_product = {
                    "course_name": course.course_name,
                    "course_short_desc": course.course_short_desc,
                    "creator": course.creator.id,
                    "category": course.category.id,
                    "created_at": course.created_at,
                    "updated_at": course.updated_at,
                }
                serialized_data.append(serialized_product)
            return Response(serialized_data, status=status.HTTP_200_OK)

        elif category_name == "ebook":
            ebooks = Ebook.objects.filter(category=category)
            serialized_data = []
            for ebook in ebooks:
                serialized_product = {
                    "name": ebook.name,
                    "no_of_chapters": ebook.no_of_chapters,
                    "no_of_pages": ebook.no_of_pages,
                    "description": ebook.description,
                    "creator": ebook.creator.id,
                    "category": ebook.category.id,
                    "created_at": ebook.created_at,
                    "updated_at": ebook.updated_at,
                    "ebook_desc": ebook.ebook_desc,
                    "level": ebook.level.id,
                }
                serialized_data.append(serialized_product)
            return Response(serialized_data, status=status.HTTP_200_OK)

        else:
            products_data = []
            products = Product.objects.all()

            for product in products:
                product_data = {
                    "id": product.id,
                    "title": product.title,
                    "credits": product.credits,
                    "creator": product.creator.id,
                    "category": product.category.id,
                    "subcategory": product.subcategory.id,
                    "product_type": product.product_type.id,
                    "created_at": product.created_at,
                    "updated_at": product.updated_at,
                    "tag": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
                    "no_of_items": product.no_of_items,
                    "is_free": product.is_free,
                    "assets": []
                }

                hero_asset = Asset.objects.filter(product=product, is_hero_img=True).first()
                if hero_asset:
                    asset_data = {
                        "id": hero_asset.id,
                        "asset": hero_asset.asset,
                        "asset_type": hero_asset.asset_type.id,
                        "meta_tag": hero_asset.meta_tag,
                        "is_hero_img": hero_asset.is_hero_img,
                        "created_at": hero_asset.created_at,
                        "updated_at": hero_asset.updated_at,
                        "is_free": hero_asset.is_free
                    }
                    product_data["assets"].append(asset_data)

                products_data.append(product_data)

        return Response(products_data)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def download_product(request):
    user = request.user 
    product_id = request.data.get('product_id')  

    if product_id is None:
        return Response({"error": "Product ID is required"}, status=400)

    
    download_product = ProductDownload.objects.create(user=user, product_id=product_id)

    return Response({"message": "Product download successfully"}, status=201)




@api_view(['GET'])
def get_subcategories(request, category_id):
    subcategories = Subcategory.objects.filter(categories=category_id)
    serialized_data = []
    for subcategory in subcategories:
        serialized_subcategory = {
            "subcategory_name": subcategory.name,
        }
        serialized_data.append(serialized_subcategory)
    return Response(serialized_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_singleproduct(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=404)

    product_data = {
        "id": product.id,
        "title": product.title,
        "credits": product.credits,
        "creator": product.creator.id,
        "category": product.category.id,
        "subcategory": product.subcategory.id,
        "product_type": product.product_type.id,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "tag": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
        "no_of_items": product.no_of_items,
        "is_free": product.is_free,
        "assets": []
    }

    assets = Asset.objects.filter(product=product)
    for asset in assets:
        asset_data = {
            "id": asset.id,
            "asset": asset.asset,
            "asset_type": asset.asset_type.id,
            "meta_tag": asset.meta_tag,
            "is_hero_img": asset.is_hero_img,
            "created_at": asset.created_at,
            "updated_at": asset.updated_at,
            "is_free": asset.is_free
        }
        product_data["assets"].append(asset_data)

    return Response(product_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_product_contain_images(request, product_id):
    assets = Asset.objects.filter(product_id=product_id)

    asset_list = []
    for asset in assets:
        asset_data = {
            'product_id': asset.product_id,
            'asset': asset.asset,
            'asset_type': asset.asset_type_id,
            'meta_tag': asset.meta_tag,
            'is_hero_img': asset.is_hero_img,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at
        }
        asset_list.append(asset_data)

    return JsonResponse({'assets': asset_list})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_for_later(request):
    user = request.user 
    product_id = request.data.get('product_id')  

    if product_id is None:
        return Response({"error": "Product ID is required"}, status=400)

    
    saved_product = SavedProduct.objects.create(user=user, product_id=product_id)

    return Response({"message": "Product saved successfully"}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creator_data(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({'error': 'Please provide user_id in the request body'}, status=400)

        product_count = Product.objects.filter(creator_id=user_id).count()
        asset_count = Asset.objects.filter(creator_id=user_id).count()
        
        return Response({
            'product_count': product_count,
            'asset_count': asset_count
        })
    else:
        return Response({'error': 'Only POST requests are allowed for this endpoint'}, status=405)
    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def most_downloaded_products(request, category_id):
    products = ProductDownload.objects.filter(product__category__id=category_id).values('product').annotate(download_count=Count('product')).order_by('-download_count')

    serialized_data = []
    for item in products:
        product = Product.objects.get(id=item['product'])

        product_data = {
            "product_id": product.id,
            "product_title": product.title,
            "credits": product.credits,
            "creator": product.creator.id,
            "category": product.category.id,
            "product_type": product.product_type.id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
            "no_of_items": product.no_of_items,
            "is_free": product.is_free,
            "assets": []
        }

        hero_asset = Asset.objects.filter(product=product, is_hero_img=True).first()
        if hero_asset:
            asset_data = {
                "id": hero_asset.id,
                "asset": hero_asset.asset,
                "asset_type": hero_asset.asset_type.id,
                "meta_tag": hero_asset.meta_tag,
                "is_hero_img": hero_asset.is_hero_img,
                "created_at": hero_asset.created_at,
                "updated_at": hero_asset.updated_at,
                "is_free": hero_asset.is_free
            }
            product_data["assets"].append(asset_data)

        serialized_data.append(product_data)

    return Response(serialized_data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def related_products(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        related_products = Product.objects.filter(category=product.category)

        data = []
        for related_product in related_products:
           product_data = {
            "product_id": product.id,
            "product_title": product.title,
            "credits": product.credits,
            "creator": product.creator.id,
            "category": product.category.id,
            "product_type": product.product_type.id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
            "no_of_items": product.no_of_items,
            "is_free": product.is_free,
            "assets": []
        }

        hero_asset = Asset.objects.filter(product=product, is_hero_img=True).first()
        if hero_asset:
            asset_data = {
                "id": hero_asset.id,
                "asset": hero_asset.asset,
                "asset_type": hero_asset.asset_type.id,
                "meta_tag": hero_asset.meta_tag,
                "is_hero_img": hero_asset.is_hero_img,
                "created_at": hero_asset.created_at,
                "updated_at": hero_asset.updated_at,
                "is_free": hero_asset.is_free
            }
            product_data["assets"].append(asset_data)
            data.append(product_data)

        return Response(data, status=200, safe=False)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def related_asset(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        related_products = Product.objects.filter(category=product.category)

        asset= []
        for related_product in related_products:
           product_data = {
            "product_id": product.id,
            "product_title": product.title,
            "credits": product.credits,
            "creator": product.creator.id,
            "category": product.category.id,
            "product_type": product.product_type.id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
            "no_of_items": product.no_of_items,
            "is_free": product.is_free,
            "assets": []
        }

        hero_asset= Asset.objects.filter(product=related_product).first()
        if hero_asset:
            asset_data = {
                "id": hero_asset.id,
                "asset": hero_asset.asset,
                "asset_type": hero_asset.asset_type.id,
                "meta_tag": hero_asset.meta_tag,
                "is_hero_img": hero_asset.is_hero_img,
                "created_at": hero_asset.created_at,
                "updated_at": hero_asset.updated_at,
                "is_free": hero_asset.is_free
            }
            asset.append(asset_data)
           
        return Response(asset, status=200)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)



#-----------------------------------Single Asset card details -------------------------------------------------------
    


@api_view(['GET'])
def related_product_for_asset(request, asset_id):
    try:
        asset = get_object_or_404(Asset, id=asset_id)
        product = asset.product

        data = []
        product_data = {
            "product_id": product.id,
            "product_title": product.title,
            "credits": product.credits,
            "creator": product.creator.id,
            "category": product.category.id,
            "product_type": product.product_type.id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
            "no_of_items": product.no_of_items,
            "is_free": product.is_free,
            "assets": []
        }

        hero_asset = Asset.objects.filter(product=product, is_hero_img=True).first()
        if hero_asset:
            asset_data = {
                "id": hero_asset.id,
                "asset": hero_asset.asset,
                "asset_type": hero_asset.asset_type.id,
                "meta_tag": hero_asset.meta_tag,
                "is_hero_img": hero_asset.is_hero_img,
                "created_at": hero_asset.created_at,
                "updated_at": hero_asset.updated_at,
                "is_free": hero_asset.is_free
            }
            product_data["assets"].append(asset_data)
            data.append(product_data)
        return Response(data)
    except Asset.DoesNotExist:
        return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def download_single_asset(request):
    user = request.user 
    asset_id = request.data.get('asset_id')  

    if asset_id is None:
        return Response({"error": "asset ID is required"}, status=400)

    
    download_product = AssetDownload.objects.create(user=user, asset_id=asset_id)

    return Response({"message": "Asset download successfully"}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_for_asset(request):
    user = request.user 
    asset_id = request.data.get('asset_id')  

    if asset_id is None:
        return Response({"error": "Asset ID is required"}, status=400)

    
    saved_product = SavedProduct.objects.create(user=user, asset_id=asset_id)

    return Response({"message": "Asset saved successfully"}, status=201)



@api_view(['POST'])
def filter_products(request):
    search_query = request.data.get('search', '')
    product_type = request.data.get('product_type', '')
    queryset = Product.objects.all()

    if search_query:
        if product_type == 'single':
            asset_queryset = Asset.objects.filter(name__icontains=search_query)
            # Return fields of Asset model for single products
            assets = [{'name': asset.name, 'asset': asset.asset, 'asset_type': asset.asset_type.name,
                       'creator': asset.creator.username, 'meta_tag': asset.meta_tag,
                       'is_hero_img': asset.is_hero_img, 'created_at': asset.created_at} for asset in asset_queryset]
            return Response({'assets': assets})
        else:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(tag__name__icontains=search_query))
    
    # Return fields of Product model for other products
    products = [{'title': product.title, 'credits': product.credits, 'creator': product.creator.username,
                 'category': product.category.name, 'subcategory': product.subcategory.name,
                 'product_type': product.product_type.name, 'created_at': product.created_at,
                 'updated_at': product.updated_at, 'tag': [tag.name for tag in product.tag.all()],
                 'no_of_items': product.no_of_items, 'is_free': product.is_free} for product in queryset]
    return Response({'products': products})

# @api_view(['POST'])
# def product_transaction_api(request):
#     if request.method == 'POST':
#         try:
#             user_id = request.data.get('user_id')
#             product_id = request.data.get('product_id')
#             purchase_amount = request.data.get('purchase_amount')

#             user =settings.AUTH_USER_MODEL.objects.get(id=user_id)
            
#             purchase_transaction_type = TransactionType.objects.get(name='purchase')
            
#             new_balance = user.balance - purchase_amount
            
#             if new_balance < 0:
#                 raise ValueError("Insufficient balance")
            
#             product_transaction = ProductTransaction.objects.create(
#                 credit_amount=0,
#                 debit_amount=purchase_amount,
#                 tran_type_id=purchase_transaction_type.id,
#                 user_id=user_id,
#                 product_id=product_id
#             )
            
#             user.balance = new_balance
#             user.save()
            
#             return Response({"message": "Purchase successful", "transaction_id": product_transaction.tran_id}, status=status.HTTP_201_CREATED)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         except TransactionType.DoesNotExist:
#             return Response({"error": "Purchase transaction type not found"}, status=status.HTTP_404_NOT_FOUND)
#         except ValueError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    

