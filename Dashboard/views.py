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
from rest_framework import status

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
#@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    try:
        product = Pack.objects.get(id=product_id)
        product.is_active= False
        product.save()
        return JsonResponse({"message": "Product soft deleted successfully"})
    except Pack.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def upload_asset(request):
    if request.method == 'POST' and request.FILES.get('image'):
        print(request.data)
        uploaded_file= request.FILES['image']
        required_fields = ['name']

        for field in required_fields:
            if field not in request.POST or not request.POST[field]:
                return JsonResponse({'error': f'{field} is required'}, status=400)
            
        if not request.FILES.getlist('image'):
            return JsonResponse({'error': 'Thumbnail image is required'}, status=400)
      
      
        credits = request.POST.get('credits', 0)
        if not credits.isdigit() or int(credits) < 0:
            return JsonResponse({'error': 'Credits must be a non-negative integer'}, status=400)

        is_active = request.POST.get('is_active', '').lower()
        if is_active not in ['true', 'false']:
            return JsonResponse({'error': 'is_active must be either true or false'}, status=400)

      



        file_name = generate_unique_filename(uploaded_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
        image= Image.objects.create(url=file_url, asset_type_id=1)
        print(image)


        pack_image_objects = []
        uploaded_files= request.FILES.getlist('files')
        print(uploaded_files)
        

        for uploaded_file in uploaded_files:
            file_name = generate_unique_filename(uploaded_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            
        
            asset_file= AssetFile.objects.create(url=file_url, asset_type_id=1)
            pack_image_objects.append(asset_file)

        
        category_id = request.POST.get('category_id')
        category = Category.objects.get(pk=category_id)

      
        P=Pack()
        P=None
        #user=request.user
        user=User.objects.first()
        asset = Asset.objects.create(
            name=request.POST.get('name'),
            pack_id=P,
            creator_id=user.id,
            credits=request.POST.get('credits', 0),
            category=category,
            is_active=request.POST.get('is_active', False),
            is_free=request.POST.get('credits', 0) == 0,
        
        )

      
        asset.image.add(image)
        print(pack_image_objects)
        asset.asset_file.add(*pack_image_objects)
        asset.save()
        asset_id=asset.id
        file_id=asset_file.id



        tag_names = request.POST.getlist('tags', [])
        if not tag_names:
            return JsonResponse({'error': 'At least one tag is required'}, status=400)

      
        tag_names = request.POST.getlist('tags', [])
        t=tag_names[0]
        ts=t.strip('[]')
        tag=ts.split(',')


        for tag_name in tag:
            tag, _ = AssetTag.objects.get_or_create(name=tag_name)
            asset.tag.add(tag)



        return JsonResponse({'message': 'Asset uploaded successfully.', 'url': file_url,'asset_id':asset_id,"file_id":file_id})
    else:
        return JsonResponse({'error': 'Please provide a file to upload.'}, status=400)



@api_view(['POST'])
def upload_pack(request):  
    data = request.data
    print(data)
    u = User.objects.first()

    required_fields = ['title', 'category_id', 'subcategory_id', 'product_type_id', 'base_price', 'discount_price', 'hero_images', 'tags']
    for field in required_fields:
        if field not in request.data:
            return JsonResponse({'error': f'{field} is required'}, status=400)

  
    numeric_fields = ['category_id', 'subcategory_id', 'product_type_id', 'base_price', 'discount_price']
    for field in numeric_fields:
        if not str(request.data.get(field)).isdigit():
            return JsonResponse({'error': f'{field} must be a valid number'}, status=400)

   
    if 'hero_images' not in request.FILES or not request.FILES.getlist('hero_images'):
        return JsonResponse({'error': 'At least one hero image is required'}, status=400)


    

    category_id = request.POST.get('category_id')
    category = Category.objects.get(pk=category_id)

    subcategory_id = request.POST.get('subcategory_id')
    subcategory = Subcategory.objects.get(pk=subcategory_id)

    product_type_id = request.POST.get('product_type_id')
    product_type = ProductType.objects.get(pk=product_type_id)
   
    pack_image_objects = []
    uploaded_files= request.FILES.getlist('hero_images')

   
 

    for uploaded_file in uploaded_files:
        file_name = generate_unique_filename(uploaded_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
        
      
        asset_file= Image.objects.create(url=file_url, asset_type_id=1)
        pack_image_objects.append(asset_file)

    title = data.get('title')
    if Pack.objects.filter(title=title).exists():
        return JsonResponse({'error': 'A pack with this title already exists'}, status=400)


    pack = Pack(
        title=request.POST.get('title'),
        creator=u,
        category=category,
        subcategory=subcategory,
        product_type=product_type,
        base_price=request.POST.get('base_price'),
        discount_price=request.POST.get('discount_price')
    )
    pack.save()

    

    print(pack.id)

    asset_ids1 = request.POST.getlist('asset_ids') 
    t=asset_ids1[0]
    ts=t.strip('[]')
    asset_ids=ts.split(',')



    if not asset_ids:
        return JsonResponse({'error': 'asset_ids required'}, status=400)


    if asset_ids: 
        for asset_id in asset_ids:
            try:
                asset = Asset.objects.get(id=asset_id)
                asset.pack = pack
                asset.save()
            except Asset.DoesNotExist:
                pass

    
    tag_names = request.POST.getlist('tags', [])
   
    t=tag_names[0]
    ts=t.strip('[]')
    tag=ts.split(',')

    for tag_name in tag:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        pack.tag.add(tag)

    pack.image.add(*pack_image_objects)
    pack.save()
          
    return JsonResponse({'message': 'pack created successfully'})

def generate_unique_filename(filename):
    import uuid
    _, ext = os.path.splitext(filename)
    return f"{uuid.uuid4()}{ext}"



@api_view(['POST'])  
def get_selected_existing(request): 
   
    user = User.objects.first()  
    data=request.data
    asset_ids1=data['asset_ids']
    print(asset_ids1)
    assets = Asset.objects.filter(id__in=asset_ids1,is_active=True)
    print(assets)

    all_assets = []

    for asset in assets:
        data = {
            "name": asset.name,
            "credits": asset.credits,
            "asset_id": asset.id, 
            "is_active": asset.is_active,
            "is_free": asset.is_free,
            "image": list(asset.image.values_list('url', flat=True)), 
            "tags": list(asset.tag.values_list('name', flat=True)),
            "asset_file": list(asset.asset_file.values_list('url', flat=True)),  
        }

        all_assets.append(data)

    return Response({"all_assets": all_assets})



@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def update_asset(request, asset_id):
    try:
        asset = Asset.objects.get(pk=asset_id)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    
    if request.method == 'PUT' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        required_fields = ['name', 'credits', 'is_active', 'tags','category_id']
        
        for field in required_fields:
            if field not in request.POST or not request.POST[field]:
                return JsonResponse({'error': f'{field} is required'}, status=400)
            
        credits = request.POST.get('credits', 0)
        if not credits.isdigit() or int(credits) < 0:
            return JsonResponse({'error': 'Credits must be a non-negative integer'}, status=400)

        is_active = request.POST.get('is_active', '').lower()
        if is_active not in ['true', 'false']:
            return JsonResponse({'error': 'is_active must be either true or false'}, status=400)

     
        file_name = generate_unique_filename(uploaded_image.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
        new_image = Image.objects.create(url=file_url, asset_type_id=1)
        
 
        asset.name = request.POST.get('name')
        asset.credits = credits
        asset.is_active = is_active == 'true'
        
        category_id = request.POST.get('category_id')
        category = Category.objects.get(pk=category_id)
        asset.category = category
        
        asset.tag.clear()
        tags = request.POST.getlist('tags', [])
        t=tags[0]
        ts=t.strip('[]')
        tag=ts.split(',')
        for tag_name in tag:
            tag_name = tag_name.strip()
            tag, _ = AssetTag.objects.get_or_create(name=tag_name)
            asset.tag.add(tag)
        
        asset.image.clear()
        asset.image.add(new_image)
        
        asset.save()

        if 'files' in request.FILES:
            uploaded_files = request.FILES.getlist('files')
            pack_image_objects = []
            for uploaded_file in uploaded_files:
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_file = AssetFile.objects.create(url=file_url, asset_type_id=1)
                pack_image_objects.append(asset_file)
            asset.asset_file.clear()
            asset.asset_file.add(*pack_image_objects)

        asset.save()
        
        return JsonResponse({'message': 'Asset updated successfully.', 'url': file_url, 'asset_id': asset_id}, status=200)
    else:
        return JsonResponse({'error': 'Please provide an image file to update.'}, status=400)


@api_view(['GET'])
def get_packs_by_title(request):
    title_query = request.GET.get('title', '')  
    packs = Pack.objects.filter(title__icontains=title_query,is_active=True)

    pack_data=[]
    
    for pack in packs:
            data={
                'title': pack.title,
                'credits': pack.credits,
                'no_of_items': pack.no_of_items,
                'is_free': pack.is_free,
                'is_active': pack.is_active,
                'base_price': pack.base_price,
                'discount_price': pack.discount_price,
                'image_urls': [image.url for image in pack.image.all()],
                'tags': [tag.name for tag in pack.tag.all()]
            } 
            pack_data.append(data)
    
    return JsonResponse({'packs':pack_data})

@api_view(['GET'])
def get_pack_data(request):
 
    packs = Pack.objects.filter(is_active=True)

    pack_data=[]
    
    for pack in packs:
            data={
                'title': pack.title,
                'credits': pack.credits,
                'no_of_items': pack.no_of_items,
                'is_free': pack.is_free,
                'is_active': pack.is_active,
                'base_price': pack.base_price,
                'discount_price': pack.discount_price,
                'image_urls': [image.url for image in pack.image.all()],
                'tags': [tag.name for tag in pack.tag.all()]
            } 
            pack_data.append(data)
    
    return JsonResponse({'packs':pack_data})


@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def delete_asset(request, asset_id):
    try:
        product = Asset.objects.get(id=asset_id)
        Asset.is_active= False
        product.save()
        return JsonResponse({"message": "Asset soft deleted successfully"})
    except Pack.DoesNotExist:
        return JsonResponse({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



