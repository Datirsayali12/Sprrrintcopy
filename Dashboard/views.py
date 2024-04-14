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
import json
from django.core.exceptions import ValidationError

        
@api_view(['POST'])
def upload_asset(request):
    if request.method == 'POST':
        data=request.data.getlist('data')
        print(data)
        
        try:
            json_data = data[0]
            data_dict = json.loads(json_data)

            asset_name = data_dict.get('name')
            print(asset_name)
            files = request.FILES.getlist('files') 
            images = request.FILES.getlist('image')  # Get the list of uploaded files

            

            required_fields = ['name', 'category_id', 'base_price', 'discount_price']
            for field in required_fields:
                if field not in data_dict or not data_dict[field]:
                    return JsonResponse({'error': f'{field} is required'}, status=400)
            
            if not files:
                return JsonResponse({'error': 'At least one file is required'}, status=400)
            
            
            
            # Handle thumbnail image uploads
            asset_hero_images = []
            for uploaded_image in images:
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
            for uploaded_file in files:
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
                category_id = data_dict.get('category_id')
                category = Category.objects.get(pk=category_id)
            except (ValueError, Category.DoesNotExist):
                return JsonResponse({'error': 'Invalid category ID'}, status=400)


          
            is_active_str = data_dict.get('is_active', '').lower()
            is_free_str = data_dict.get('is_free', '').lower()

            # Convert string values to boolean
            is_active = is_active_str == 'true'
            is_free = is_free_str == 'true'

            # Validate boolean values
            if is_active_str not in ['true', 'false']:
                return JsonResponse({'error': 'is_active must be either true or false'}, status=400)

            if is_free_str not in ['true', 'false']:
                return JsonResponse({'error': 'is_free must be either true or false'}, status=400)


                    
            user = User.objects.first() 
            asset = Asset.objects.create(
                name=data_dict.get('name'),
                creator=user,
                base_price=data_dict.get('base_price'),
                discount_price=data_dict.get('discount_price'),
                category=category,
                is_active=is_active,
                is_free=is_free
            )
            asset.save()
        
            asset.image.add(*asset_hero_images)
            asset.save()
            asset.asset_file.add(*file_objects)
            asset.save()

    
            tag_names = data_dict.get('tags', [])
            if not tag_names:
                return JsonResponse({'error': 'At least one tag is required'}, status=400)
            
            
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                asset.tags.add(tag)

           
            return JsonResponse({'message': 'Asset uploaded successfully.', 'asset_id': asset.id,"file_id":asset_file.id,"file_url":asset_file.url}, status=201,safe=False)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


    
@api_view(['POST'])
def create_from_existing(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        required_fields = ['name', 'asset_id', 'base_price', 'discount_price', 'is_free', 'is_active']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        asset_id = data['asset_id']

        try:
            existing_asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return JsonResponse({'error': 'Asset does not exist'}, status=404)
        
        # Convert string values to boolean
        is_active = data['is_active'].lower() == 'true'
        is_free = data['is_free'].lower() == 'true'

        # Validate boolean values
        if is_active not in [True, False]:
            return JsonResponse({'error': 'is_active must be either true or false'}, status=400)

        if is_free not in [True, False]:
            return JsonResponse({'error': 'is_free must be either true or false'}, status=400)

        if (existing_asset.name == data['name'] and
            existing_asset.base_price == data['base_price'] and
            existing_asset.discount_price == data['discount_price'] and
            existing_asset.is_free == is_free and
            existing_asset.is_active == is_active):

            return JsonResponse({'existing_asset_id': existing_asset.id}, status=200)
        else:
    
            creator = User.objects.first()

            new_asset = Asset.objects.create(
                name=data['name'],
                creator=creator,
                base_price=data['base_price'],
                discount_price=data['discount_price'],
                category=existing_asset.category,
                is_free=is_free,
                is_active=is_active
            )

            for image in existing_asset.image.all():
                new_asset.image.add(image)

            for asset_file in existing_asset.asset_file.all():
                new_asset.asset_file.add(asset_file)

            return JsonResponse({'created_asset_id': new_asset.id}, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    #name,credits,asset_id,is_free=False
    #get asset instance from asset_id
    #get_all required fields from instance
    #create new asset
    #add all fields from payload and asset instance
    #save()




 
@api_view(['POST'])
def upload_pack(request):
    #['{"title": "pack23","base_price":100,"discount_price": 10,"tags": ["tag1","tag2"],"asset_ids": [2],"category_id": 1}']
    #{'title': ['pack16'], 'base_price': ['100'], 'discount_price': ['10'], 'tags': ['tag1,tag2'], 'asset_ids': ['1,2'], 'category_id': ['1'], 'total_assets': ['10'], 'hero_images': [<InMemoryUploadedFile: file1.txt (text/plain)>]}
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data=request.data.getlist('data')
        print(data)
        json_data = data[0]
        data_dict = json.loads(json_data)
        u = User.objects.first()
        print(data_dict)

        required_fields = ['title', 'category_id','base_price', 'discount_price','tags']
        for field in required_fields:
            if field not in data_dict:
                return JsonResponse({'error': f'{field} is required'}, status=400)

        numeric_fields = ['category_id', 'base_price', 'discount_price']
        for field in numeric_fields:
            if not str(data_dict[field]).isdigit():
                return JsonResponse({'error': f'{field} must be a valid number'}, status=400)

        if 'hero_images' not in request.FILES or not request.FILES.getlist('hero_images'):
            return JsonResponse({'error': 'At least one hero image is required'}, status=400)

        category_id = data_dict['category_id']
        category = Category.objects.get(pk=category_id)

        

        pack_image_objects = []
        uploaded_files = request.FILES.getlist('hero_images')
        print(uploaded_files)

        for uploaded_file in uploaded_files:
            file_name = generate_unique_filename(uploaded_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

    

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            asset_file,_ = Image.objects.get_or_create(url=file_url)
            pack_image_objects.append(asset_file)

        title = data_dict.get('title')
        if Pack.objects.filter(title=title).exists():
            return JsonResponse({'error': 'A pack with this title already exists'}, status=400)

        pack = Pack(
            title=data_dict.get('title'),
            creator=u,
            category=category,
            base_price=data_dict.get('base_price'),
            discount_price=data_dict.get('discount_price'),
        )
        pack.save()
       
        asset_ids = data_dict.get('asset_ids') 
        if asset_ids: 
            for asset_id in asset_ids:
                try:
                    asset = Asset.objects.get(id=int(asset_id))
                    pack.assets.add(asset)
                    
                except Asset.DoesNotExist:
                    pass
            pack.save()

        tag_names = data_dict.get('tags', [])
        print(tag_names)
       
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            pack.tags.add(tag)

        print(pack.tags.name)

        pack.image.add(*pack_image_objects)
        pack.save()

        total_assets =pack.assets.count()
        pack.total_assets=total_assets
        pack.save()



        return JsonResponse({'message': 'Pack created successfully',"pack_id":pack.id})
    
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
    if request.method == 'PUT':
        data=request.data.getlist('data')
        print(data)
        json_data = data[0]
        data_dict = json.loads(json_data)
        print(data_dict)
        files = request.FILES.getlist('files') 
        images = request.FILES.getlist('image') 

        print(files)
        print(images)

        try:
            asset = Asset.objects.get(pk=asset_id)

            # Update asset fields
            asset.name = data_dict.get('name', asset.name)
            asset.base_price = data_dict.get('base_price', asset.base_price)
            asset.discount_price = data_dict.get('discount_price', asset.discount_price)

            category_id = data_dict.get('category_id', asset.category.id)
            try:
                category = Category.objects.get(pk=category_id)
                asset.category = category
            except (ValueError, Category.DoesNotExist):
                return JsonResponse({'error': 'Invalid category ID'}, status=400)

            is_active_str = data_dict.get('is_active', '')
            is_free_str = data_dict.get('is_free', '')

            is_active = is_active_str == 'true'
            is_free = is_free_str == 'true'

            print(is_active)
            print(is_free)

            asset.is_active=is_active
            asset.is_free=is_free

            asset.save()

            # Clear existing files
            asset.asset_file.clear()
          
            for uploaded_file in files:
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
               
                asset_type, _ = AssetType.objects.get_or_create(name=os.path.splitext(file_name)[1].lower())
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_file = AssetFile.objects.create(url=file_url, asset_type=asset_type)
                asset.asset_file.add(asset_file)
                asset.save()

            asset.image.clear()
            # Handle image uploads
            for uploaded_image in images:
                file_name = generate_unique_filename(uploaded_image.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_image.chunks():
                        destination.write(chunk)
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_image = Image.objects.create(url=file_url)
                asset.image.add(asset_image)
                asset.save()

            return JsonResponse({'message': 'Asset updated successfully.', 'asset_id': asset.id}, status=200)

        except Asset.DoesNotExist:
            return JsonResponse({'error': 'Asset not found'}, status=404)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    



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
def get_packs_by_title_or_tag(request):
    query = request.GET.get('query', '')

    packs = Pack.objects.filter(is_active=True)

    if query:
        packs = packs.filter(Q(title__icontains=query) | Q(tags__name__icontains=query))

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
    query = request.GET.get('query', '')

  
    assets = Asset.objects.filter(
        Q(name__icontains=query) | Q(tags__name__icontains=query)
    ).distinct()
    u=User.objects.first()

   
    assets_data = []
    for asset in assets:
        asset_data = {
            'id': asset.id,
            'name': asset.name,
            'creator': u.id,
            'category': asset.category.name,
            'is_free': asset.is_free,
            'is_active': asset.is_active,
        }
        assets_data.append(asset_data)

    return JsonResponse({'assets': assets_data})



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
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        pack = Pack.objects.get(pk=pack_id)
        data = request.data.getlist('data')
        json_data = data[0]
        data_dict = json.loads(json_data)


        pack.title = data_dict.get('title', pack.title)
        pack.base_price = data_dict.get('base_price', pack.base_price)
        pack.discount_price = data_dict.get('discount_price', pack.discount_price)

    
        category_id = data_dict.get('category_id', pack.category.id)
        category = Category.objects.get(pk=category_id)
        pack.category = category

        # Update assets
        asset_ids = data_dict.get('asset_ids', [])
        pack.assets.clear()  
        for asset_id in asset_ids:
            try:
                asset = Asset.objects.get(pk=int(asset_id))
                pack.assets.add(asset)
            except Asset.DoesNotExist:
                pass
        pack.save()
      
        tag_names = data_dict.get('tags', [])
        pack.tags.clear() 
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            pack.tags.add(tag)
        pack.save()

        if 'hero_images' in request.FILES and request.FILES.getlist('hero_images'):
            pack.image.clear()  
            uploaded_files = request.FILES.getlist('hero_images')
            pack_image_objects = []
            for uploaded_file in uploaded_files:
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                image, _ = Image.objects.get_or_create(url=file_url)
                pack_image_objects.append(image)
            pack.image.add(*pack_image_objects)
        pack.save()

      
        total_assets = pack.assets.count()
        pack.total_assets = total_assets

        pack.save()

        return JsonResponse({'message': 'Pack updated successfully', 'pack_id': pack.id})

    except Pack.DoesNotExist:
        return JsonResponse({'error': 'Pack not found'}, status=404)

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



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
                "base_price":asset.base_price,
                "discount_price":asset.discount_price,
                "hero_images":[image.url for image in asset.image.all()],
                "asset_files":[file.url  for file in asset.asset_file.all()],
                "tags":[tag.name for tag in asset.tags.all()]
                
            }
            all_assets.append(data)
        return JsonResponse({'all_assets':all_assets}, status=200)













