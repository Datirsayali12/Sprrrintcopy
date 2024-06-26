from rest_framework.decorators import api_view,permission_classes
from UIAsset.models import *
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
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import os

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
def get_all_data(request, product_type):

    if product_type=="pack":
        assets = Asset.objects.all()
        asset_data = []
        for asset in assets:
            asset_dict = {
                'id': asset.id,
                'name': asset.name,
                'pack_id': asset.pack.title if asset.pack else None,
                'creator_id': asset.creator_id,
                'is_free': asset.is_free,
                'credits': asset.credits,
                'tags': list(asset.tag.values_list('name', flat=True)),
                'images': list(asset.image.values_list('url', flat=True)),
            }
            asset_data.append(asset_dict)
        
        packs = Pack.objects.all()
        pack_data = []
        for pack in packs:
            pack_dict = {
                'id': pack.id,
                'title': pack.title,
                'credits': pack.credits,
                'creator_id': pack.creator_id,
                'category_id': pack.category_id,
                'product_type_id': pack.product_type_id,
                'no_of_items': pack.no_of_items,
                'is_free': pack.is_free,
                'base_price': pack.base_price,
                'discount_price': pack.discount_price,
                'tags': list(pack.tag.values_list('name', flat=True)),
                'images': list(pack.image.values_list('url', flat=True)),
            }
            pack_data.append(pack_dict)

        return JsonResponse({'packs': pack_data,'assets': asset_data})
    elif product_type=="single":
        assets = Asset.objects.filter(pack=None)
        asset_data = []
        for asset in assets:
            asset_dict = {
                'id': asset.id,
                'name': asset.name,
                'creator_id': asset.creator_id,
                'is_free': asset.is_free,
                'credits': asset.credits,
                'tags': list(asset.tag.values_list('name', flat=True)),
                'images': list(asset.image.values_list('url', flat=True)),
            }
            asset_data.append(asset_dict)
        return JsonResponse({'packs': pack_data,'assets': asset_data})



@api_view(['POST'])
def get_tag_and_category(request):
    categories=Category.objects.all()
    category_names=[{"category_id":i.id, "category_name":i.name} for i in categories]

    tags=Tag.objects.all()
    tag_names=[ {"tag_id":i.id,"tag_name":i.name } for i in tags]

    data={
        'categories':category_names,
        'tags':tag_names
    }

    return JsonResponse({'data':data}, status=200)







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
    


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def upload_asset(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        file_name = generate_unique_filename(uploaded_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
        
      
        asset_type_id = request.POST.get('asset_type_id') 
        asset_file= AssetFile.objects.create(url=file_url, asset_type_id=asset_type_id)

      
        P=Pack()
        P=None
        #user=request.user
        user=User.objects.first()
        asset = Asset.objects.create(
            name=request.POST.get('name'),
            pack_id=P,
            creator_id=user.id,
            credits=request.POST.get('credits', 0),
            is_active=request.POST.get('is_active', False),
            is_free=request.POST.get('credits', 0) == 0
        )

    
        asset.asset_file.add(asset_file)
        asset_id=asset.id
        file_id=asset_file.id
      
        tag_names = request.POST.getlist('tags', [])
        for tag_name in tag_names:
            tag, _ = AssetTag.objects.get_or_create(name=tag_name)
            asset.tag.add(tag)

        return JsonResponse({'message': 'Asset uploaded successfully.', 'url': file_url,'asset_id':asset_id,"file_id":file_id})
    else:
        return JsonResponse({'error': 'Please provide a file to upload.'}, status=400)

def generate_unique_filename(filename):
    import uuid
    _, ext = os.path.splitext(filename)
    return f"{uuid.uuid4()}{ext}"





# @api_view(['POST'])
# def upload_pack(request):  
#     data = request.data
#     u = User.objects.first()

#     pack_data = data.get('pack', {})
#     category = Category.objects.first()
#     subcategory = Subcategory.objects.first()
#     product_type=ProductType.objects.first()
   
#     pack_image_objects = []
#     for uploaded_file in request.FILES.getlist('images'):
#         file_name = generate_unique_filename(uploaded_file.name)
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#         with open(file_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)

#         file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
#         asset_type, _ = AssetType.objects.get_or_create(type='Image')
#         image_object = Image.objects.create(url=file_url, asset_type=asset_type)
#         pack_image_objects.append(image_object)

#     pack = Pack(
#         title=request.POST.get('title'),
#         creator=u,
#         category=category,
#         subcategory=subcategory ,
#         product_type=product_type,
#         base_price=request.POST.get('base_price'),
#         discount_price=request.POST.get('discount_price')
#     )
#     pack.save()

#     for tag_id in pack_data.get('tagids', []):
#         tag, _ = Tag.objects.get_or_create(name=tag_id)
#         pack.tag.add(tag)

#     pack.image.add(*pack_image_objects)
#     pack.save()

#     return JsonResponse({'message': 'Asset uploaded successfully.', 'url': file_url})
    

# def generate_unique_filename(filename):
#     import uuid
#     _, ext = os.path.splitext(filename)
#     return f"{uuid.uuid4()}{ext}"


   
    