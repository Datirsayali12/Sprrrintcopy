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
from django.db.models import Q


        
@api_view(['POST'])
def upload_asset(request):
    if request.method == 'POST':
        try:
            required_fields = ['name', 'category_id', 'credits']
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
                return JsonResponse({'error': 'is_active must be either true or false'})
            
            
            # Handle thumbnail image uploads
            asset_hero_images = []
            for uploaded_image in request.FILES.getlist('image'):
                file_name = generate_unique_filename(uploaded_image.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_image.chunks():
                        destination.write(chunk)
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_image = Image.objects.create(url=file_url)
                asset_hero_images.append(asset_image)

            # Handle other file uploads
            file_objects = []
            for uploaded_file in request.FILES.getlist('files'):
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                if file_name.endswith(".jpg") :
                    asset_type,is_created=AssetType.objects.get_or_create(name=".jpg")
                elif file_name.endswith(".jpeg") :
                    asset_type,is_created=AssetType.objects.get_or_create(name=".jpeg")
                elif file_name.endswith(".png") :
                    asset_type,is_created=AssetType.objects.get_or_create(name=".png")
                else:
                    return JsonResponse({'message': 'Invalid File type'}, status=400, safe=False)


                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_file = AssetFile.objects.create(url=file_url, asset_type=asset_type)
                file_objects.append(asset_file)

       
            try:
                category_id = int(request.POST.get('category_id'))
                category = Category.objects.get(pk=category_id)
            except (ValueError, Category.DoesNotExist):
                return JsonResponse({'error': 'Invalid category ID'}, status=400)

         
            user = User.objects.first() 
            asset = Asset.objects.create(
                name=request.POST.get('name'),
                pack=None, 
                creator=user,
                credits=int(request.POST.get('credits', 0)),
                category=category,
                is_active=request.POST.get('is_active'),
                is_free=request.POST.get('credits', 0) == 0
            )

        
            asset.image.add(*asset_hero_images)
            asset.asset_file.add(*file_objects)
            asset.save()

    
            tag_names = request.POST.get('tags', [])
            if not tag_names:
                return JsonResponse({'error': 'At least one tag is required'}, status=400)
            
           
            print(tag_names)
            tags=tag_names.split(',')
            
            for tag_name in tags:
                tags, _ = Tag.objects.get_or_create(name=tag_name)
                asset.tags.add(tags)

           
            return JsonResponse({'message': 'Asset uploaded successfully.', 'asset_id': asset.id,"file_id":asset_file.id,"file_url":asset_file.url}, status=201,safe=False)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['POST'])
def upload_pack(request):
    #{'title': ['pack16'], 'base_price': ['100'], 'discount_price': ['10'], 'tags': ['tag1,tag2'], 'asset_ids': ['1,2'], 'category_id': ['1'], 'total_assets': ['10'], 'hero_images': [<InMemoryUploadedFile: file1.txt (text/plain)>]}
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = request.data
        u = User.objects.first()
        print(data)

        required_fields = ['title', 'category_id','base_price', 'discount_price', 'hero_images', 'tags', 'total_assets']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        numeric_fields = ['category_id', 'base_price', 'discount_price', 'total_assets']
        for field in numeric_fields:
            if not str(data.get(field)).isdigit():
                return JsonResponse({'error': f'{field} must be a valid number'}, status=400)

        if 'hero_images' not in request.FILES or not request.FILES.getlist('hero_images'):
            return JsonResponse({'error': 'At least one hero image is required'}, status=400)

        category_id = data.get('category_id')
        category = Category.objects.get(pk=category_id)

        

        pack_image_objects = []
        uploaded_files = request.FILES.getlist('hero_images')

        for uploaded_file in uploaded_files:
            file_name = generate_unique_filename(uploaded_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            
            # if file_name.endswith(".jpg") :
            #     asset_type,is_created=AssetType.objects.get_or_create(name=".jpg")
            # elif file_name.endswith(".jpeg") :
            #     asset_type,is_created=AssetType.objects.get_or_create(name=".jpeg")
            # elif file_name.endswith(".png") :
            #     asset_type,is_created=AssetType.objects.get_or_create(name=".png")
            # else:
            #     return JsonResponse({"msg:Invalid File type"})

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            asset_file = Image.objects.create(url=file_url)
            pack_image_objects.append(asset_file)

        title = data.get('title')
        if Pack.objects.filter(title=title).exists():
            return JsonResponse({'error': 'A pack with this title already exists'}, status=400)

        pack = Pack(
            title=data.get('title'),
            creator=u,
            category=category,
            base_price=data.get('base_price'),
            discount_price=data.get('discount_price'),
            total_assets=data.get('total_assets')
        )
        pack.save()

        # asset_ids = data.get('asset_ids')
        # if .objects.filter(title=title).exists():
        #     return JsonResponse({'error': 'A pack with this title already exists'}, status=400)

        # title or credits from where to get to create new asset if chnage made in existing 
       
        asset_ids = data.get('asset_ids') 
        print(type(asset_ids))
        asset_ids1=asset_ids.split(',')
        if asset_ids1: 
            for asset_id in asset_ids1:
                try:
                    asset = Asset.objects.get(id=int(asset_id))
                    pack.assets.add(asset)
                    
                except Asset.DoesNotExist:
                    pass
            pack.save()

        tag_names = data.get('tags', [])
        print(tag_names)
        tags=tag_names.split(',')

        print(tags)
       
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            pack.tags.add(tag)

        print(pack.tags.name)

        pack.image.add(*pack_image_objects)
        pack.save()

        return JsonResponse({'message': 'Pack created successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
def update_asset(request, asset_id):
    try:
        asset = Asset.objects.get(pk=asset_id)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    required_fields = ['name', 'credits', 'is_active', 'tags', 'category_id']
    
    for field in required_fields:
        if field not in request.data or not request.data[field]:
            return JsonResponse({'error': f'{field} is required'}, status=400)
        
    credits = request.data.get('credits', '0')
    if not credits.isdigit() or int(credits) < 0:
        return JsonResponse({'error': 'Credits must be a non-negative integer'}, status=400)

    is_active = request.data.get('is_active', '').lower()
    if is_active not in ['true', 'false']:
        return JsonResponse({'error': 'is_active must be either true or false'}, status=400)

    asset.name = request.data.get('name')
    asset.credits = credits
    asset.is_active = is_active == 'true'
    
    category_id = request.data.get('category_id')
    category = Category.objects.get(pk=category_id)
    asset.category = category
    
   
    uploaded_images = request.FILES.getlist('image')
    if uploaded_images:
        asset.image.clear()
        for uploaded_image in uploaded_images:
            file_name = generate_unique_filename(uploaded_image.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            asset_image = Image.objects.create(url=file_url, asset_type_id=1)
            asset.image.add(asset_image)


    uploaded_files = request.FILES.getlist('files')
    if uploaded_files:
        asset.asset_file.clear()
        for uploaded_file in uploaded_files:
            file_name = generate_unique_filename(uploaded_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            asset_file = AssetFile.objects.create(url=file_url, asset_type_id=1)
            asset.asset_file.add(asset_file)

    asset.save()
    
    asset.tag.clear()
    tag_names =request.data.getlist('tags', [])
    t=tag_names[0]
    ts=t.strip('[]')
    tags=ts.split(',')

    for tag_name in tags:
        tag_name = tag_name.strip()
        tag, _ = AssetTag.objects.get_or_create(name=tag_name)
        asset.tag.add(tag)
    asset.save()
    
    return JsonResponse({'message': 'Asset updated successfully.'}, status=200)


@api_view(['GET'])
def get_all_packs(request):
 
    packs = Pack.objects.filter(is_active=True)

    pack_data=[]
    
    for pack in packs:
            data={
                'title': pack.title,
                'no_of_items': pack.total_assets,
                'is_free': pack.is_free,
                'is_active': pack.is_active,
                'base_price': pack.base_price,
                'discount_price': pack.discount_price,
                'image_urls': [image.url for image in pack.image.all()],
                'tags': [tag.name for tag in pack.tags.all()]
            } 
            pack_data.append(data)
    
    return JsonResponse({'packs':pack_data})


@api_view(['GET'])
def get_packs_by_title_and_tag(request):
    title_query = request.GET.get('title', '')
    tag_query = request.GET.get('tag', '')

    packs = Pack.objects.filter(is_active=True)

    if title_query or tag_query:
        packs = packs.filter(Q(title__icontains=title_query) | Q(tags__name__icontains=tag_query))

    pack_data = []

    for pack in packs:
        data = {
            'title': pack.title,
            'no_of_items': pack.total_assets,
            'is_free': pack.is_free,
            'is_active': pack.is_active,
            'base_price': pack.base_price,
            'discount_price': pack.discount_price,
            'image_urls': [image.url for image in pack.image.all()],
            'tags': [tag.name for tag in pack.tags.all()]
        }
        pack_data.append(data)

    return JsonResponse({'packs': pack_data})



@api_view(['GET'])
def get_assets_by_title_and_tag(request):
    title_query = request.GET.get('title', '')
    tag_query = request.GET.get('tag', '')

    asset = Asset.objects.all()

    if title_query or tag_query:
        assets = asset.filter(Q(name__icontains=title_query) | Q(tags__name__icontains=tag_query))

    pack_data = []

    for asset in assets:
        data = {
            "id":asset.id,
            "name":asset.name,
            "category":asset.category.name,
            "creator":u.id,
            "credits":asset.credits,
            "hero_images":[image.url for image in asset.image.all()],
            "asset_files":[file.url  for file in asset.asset_file.all()],
            "tags":[ tag.name for tag in asset.tags.all()]
        }
        pack_data.append(data)

    return JsonResponse({'packs': pack_data})



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





@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def delete_asset(request, asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
        asset.is_active= False
        asset.save()
        return JsonResponse({"message": "Asset soft deleted successfully"})
    except Pack.DoesNotExist:
        return JsonResponse({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['PUT'])
def update_pack(request, pack_id):
    try:
        pack = Pack.objects.get(pk=pack_id)
    except Pack.DoesNotExist:
        return JsonResponse({'error': 'Pack not found'}, status=404)

    data = request.data

    required_fields = ['title', 'category_id', 'product_type', 'base_price', 'discount_price', 'hero_images', 'tags', 'no_of_items']
    for field in required_fields:
        if field not in request.data:
            return JsonResponse({'error': f'{field} is required'}, status=400)

    numeric_fields = ['category_id', 'base_price', 'discount_price', 'no_of_items']
    for field in numeric_fields:
        if not str(request.data.get(field)).isdigit():
            return JsonResponse({'error': f'{field} must be a valid number'}, status=400)

    if 'hero_images' not in request.FILES or not request.FILES.getlist('hero_images'):
        return JsonResponse({'error': 'At least one hero image is required'}, status=400)

    try:
        category_id = int(request.data.get('category_id'))
        category = Category.objects.get(pk=category_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid category ID'}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    product_type = request.data.get('product_type')
    try:
        product_type_instance = ProductType.objects.get(type=product_type)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product type not found'}, status=404)

    
    uploaded_images = request.FILES.getlist('hero_images')
    if uploaded_images:
        existing_images = list(pack.image.all())
        new_images = []
        for uploaded_image in uploaded_images:
            file_name = generate_unique_filename(uploaded_image.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)
            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            asset_file, created = Image.objects.get_or_create(url=file_url, asset_type_id=1)
            new_images.append(asset_file)

    
        images_to_remove = set(existing_images) - set(new_images)
        for image_to_remove in images_to_remove:
            pack.image.remove(image_to_remove)

       
        images_to_add = set(new_images) - set(existing_images)
        for image_to_add in images_to_add:
            pack.image.add(image_to_add)

  
    tag_names =request.data.getlist('tags', [])
    t=tag_names[0]
    ts=t.strip('[]')
    tags=ts.split(',')
    pack.tag.clear()
    print(tags)
    for tag_name in tags:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        pack.tag.add(tag)
    

 
    pack.title = data.get('title')
    pack.category = category
    pack.product_type = product_type_instance
    pack.base_price = int(request.data.get('base_price'))
    pack.discount_price = int(request.data.get('discount_price'))
    pack.no_of_items = int(request.data.get('no_of_items'))
    pack.save()

    return JsonResponse({'message': 'Pack updated successfully'})



@api_view(['GET'])
def get_tag_and_category(request):
    categories=Category.objects.all()
    category_names=[{"category_id":i.id, "category_name":i.name} for i in categories]

    tags=Tag.objects.all()
    tag_names=[{"tag_id":i.id, "tag_names":i.name} for i in tags]

    

    data={
        'categories':category_names,
        'tags':tag_names
    }

    return JsonResponse({'data':data}, status=200)




@api_view(['GET'])
def get_all_assets(request):
    if request.method == 'GET':
        assets=Asset.objects.all()
        u=User.objects.first()
        all_assets=[]
        for asset in assets:
            data={
                "id":asset.id,
                "name":asset.name,
                "category":asset.category.name,
                "creator":u.id,
                "credits":asset.credits,
                "hero_images":[image.url for image in asset.image.all()],
                "asset_files":[file.url  for file in asset.asset_file.all()],
                "tags":[tag.name for tag in asset.tags.all()]
                
            }
            all_assets.append(data)
        return JsonResponse({'all_assets':all_assets}, status=200)













