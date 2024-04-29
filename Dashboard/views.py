from rest_framework.decorators import api_view,permission_classes
from UIAsset.models import *
from django.http import JsonResponse
from Learn.models import *
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import *
import os
from rest_framework import status
from django.db.models import Q
import json
from django.core.exceptions import ValidationError
from zipfile import ZipFile
from django.db import IntegrityError
from rest_framework.permissions import AllowAny

#@permission_classes([IsAuthenticated])
from django.db import IntegrityError

@api_view(['POST'])
def upload_asset(request):
    if request.method == 'POST':
        data = request.data.get('data')
        data_dict = json.loads(data)

        try:
            asset_name = data_dict.get('name')
            print(asset_name)
            files = request.FILES.getlist('asset_files')
            images = request.FILES.getlist('thumbnail_images')

            # check required fields
            required_fields = ['name', 'category_id', 'credits']
            for field in required_fields:
                if field not in data_dict or not data_dict[field]:
                    return JsonResponse({'error': f'{field} is required'}, status=400)

            try:
                category_id = data_dict.get('category_id')
                category = Category.objects.get(pk=category_id)
            except (ValueError, Category.DoesNotExist):
                return JsonResponse({'error': 'Invalid category ID'}, status=400)

            # hero images uploads
            asset_hero_images = []
            for uploaded_image in images:
                file_name = generate_unique_filename(uploaded_image.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_image.chunks():
                        destination.write(chunk)
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_image = Image.objects.create(url=file_url)
                asset_image.is_hero = True
                asset_image.save()
                asset_hero_images.append(asset_image)

            # asset files upload
            file_objects = []
            for uploaded_file in files:
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # check if file is zip or not
                if not file_name.endswith(".zip"):
                    file_name = os.path.splitext(file_name)[0]

                zip_file_path = os.path.join(settings.MEDIA_ROOT, f"{file_name}.zip")
                with ZipFile(zip_file_path, 'w') as zipf:
                    zipf.write(file_path, arcname=os.path.basename(file_name))

                file_name += ".zip"
                asset_type, _ = AssetType.objects.get_or_create(name=".zip")

                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_file = AssetFile.objects.create(url=file_url, asset_type=asset_type)
                file_objects.append(asset_file)

            # asset creation
            is_free = data_dict.get('is_free', False)
            print(is_free)

            user = User.objects.first()
            asset = Asset.objects.create(
                name=data_dict.get('name'),
                creator=user,
                base_price=data_dict.get('credits'),
                category=category,
                is_free=is_free
            )
            asset.save()

            # add hero images and asset files to asset
            asset.image.add(*asset_hero_images)
            asset.save()
            asset.asset_file.add(*file_objects)
            asset.save()

            # add tags
            tag_names = data_dict.get('tags', [])
            for tag_name in tag_names:
                # Check if the tag already exists
                tag, created = Tag.objects.get_or_create(name=tag_name)
                if not created:
                    # If the tag already exists, no need to create a new one, just use the existing tag
                    asset.tags.add(tag)
            asset.save()

            return JsonResponse({'message': 'Asset uploaded successfully.', 'status': 'true', 'asset_id': asset.id}, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return JsonResponse({'error': 'Asset with this name already exists.', 'status': 'false'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_from_existing(request):
    if request.method == 'POST':
        data = request.data

        # Check for required fields
        required_fields = ['name', 'asset_id', 'credits']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        asset_id = data.get('asset_id', '')

        try:
            existing_asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return JsonResponse({'error': 'Asset does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Set default value for is_free if not provided
        is_free = data.get('is_free', False)
        user=User.objects.first()
        #create new asset
        try:
            new_asset = Asset.objects.create(
                name=data.get('name', ''),
                # creator=request.user,
                creator=user,
                base_price=data.get('credits', 0),
                category=existing_asset.category,
                is_free=is_free,
            )

            #add existing images in new_asset
            for image in existing_asset.image.all():
                new_asset.image.add(image)

            # add existing asset_files in new_asset
            for asset_file in existing_asset.asset_file.all():
                new_asset.asset_file.add(asset_file)

            return JsonResponse({'created_asset_id': new_asset.id,'status':'true'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #name,credits,asset_id,is_free=False
    #get asset instance from asset_id
    #get_all required fields from instance
    #create new asset
    #add all fields from payload and asset instance
    #save()


#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_pack(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = request.data.get('data')
        data_dict = json.loads(data)
        slider_images = request.FILES.getlist('slider_images')
        print(slider_images)
        no_of_styles=data_dict.get('no_of_styles')

        required_fields = ['name', 'category_id', 'credits', 'tags', 'is_free']
        for field in required_fields:
            if field not in data_dict:
                return JsonResponse({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        numeric_fields = ['category_id', 'credits']
        for field in numeric_fields:
            if not str(data_dict.get(field)).isdigit():
                return JsonResponse({'error': f'{field} must be a valid number'}, status=status.HTTP_400_BAD_REQUEST)

        if 'hero_images' not in request.FILES or not request.FILES.getlist('hero_images'):
            return JsonResponse({'error': 'At least one hero image is required'}, status=status.HTTP_400_BAD_REQUEST)

        category_id = data_dict['category_id']
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Invalid category ID'}, status=status.HTTP_400_BAD_REQUEST)

        #add preview images for font category

        preview_images_objects = []
        preview_images = request.FILES.getlist('preview_images')

        for uploaded_file in preview_images:
            file_name = generate_unique_filename(uploaded_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            image, _ = Image.objects.get_or_create(url=file_url)
            image.is_preview = True
            image.save()
            preview_images_objects.append(image)



        #upload pack hero images
        pack_hero_images_objects = []
        hero_images = request.FILES.getlist('hero_images')

        for uploaded_file in hero_images:
            file_name = generate_unique_filename(uploaded_file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            image, _ = Image.objects.get_or_create(url=file_url)
            image.is_hero=True
            image.save()
            pack_hero_images_objects.append(image)

        #upload pack slider images
        pack_slider_images = []
        for slider_image in slider_images:
            file_name = generate_unique_filename(slider_image.name)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in slider_image.chunks():
                    destination.write(chunk)
            file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
            asset_image = Image.objects.create(url=file_url)
            asset_image.is_hero = False
            asset_image.save()
            pack_slider_images.append(asset_image)

        #pack creation
        is_free = data_dict['is_free']
        name = data_dict.get('name')
        if Pack.objects.filter(name=name).exists():
            return JsonResponse({'error': 'A pack with this title already exists','status':'false'}, status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.first()
        pack = Pack(
            name=data_dict.get('name'),
            #creator=request.user,
            creator=user,
            category=category,
            base_price=data_dict.get('credits'),
            is_free=is_free
        )
        pack.save()

        #add assets in pack
        asset_ids = data_dict.get('asset_ids', [])
        for asset_id in asset_ids:
            try:
                asset = Asset.objects.get(id=int(asset_id))
                pack.assets.add(asset)
            except Asset.DoesNotExist:
                pass
        #add tags
        tag_names = data_dict.get('tags', [])
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            pack.tags.add(tag)

        pack.image.add(*pack_hero_images_objects)
        pack.save()
        pack.image.add(*pack_slider_images)
        pack.save()
        pack.image.add(*preview_images_objects)
        pack.save()
        total_assets = pack.assets.count()
        pack.total_assets = total_assets
        pack.save()

        # #fonts number of styles
        # pack.total_assets=no_of_styles
        # pack.save()

        return JsonResponse({'message': 'Pack created successfully', 'pack_id': pack.id,'total_assets':total_assets,'status':'true'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_unique_filename(filename):
    import uuid
    _, ext = os.path.splitext(filename)
    return f"{uuid.uuid4()}{ext}"

#@permission_classes([IsAuthenticated])
@api_view(['POST'])   # get selected existing asset details
def get_selected_existing(request):
    user = User.objects.first()  
    data=request.data
    asset_ids1=data['asset_ids']
    print(asset_ids1)
    # assets = Asset.objects.filter(id__in=asset_ids1,is_active=True,creator=request.user.id)
    assets = Asset.objects.filter(id__in=asset_ids1, is_active=True)
    print(assets)

    all_assets = []

    for asset in assets:
        data = {
            "name": asset.name,
            "credits": asset.base_price,
            "asset_id": asset.id, 
            "is_active": asset.is_active,
            "is_free": asset.is_free,
            "hero_images": [{"image_id":image.id,"image_url":image.url } for image in asset.image.all()],
            "tags": [{"tag_id":tag.id,"tag_name":tag.name } for tag in asset.tags.all()],
            "asset_file":[{"file_id":file.id,"file_url":file.url } for file in asset.asset_file.all()],
        }

        all_assets.append(data)

    return JsonResponse({"all_assets": all_assets},status=status.HTTP_200_OK)


#@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_asset(request):
    if request.method == 'PUT':
        try:
            data = request.data.get('data')
            data_dict = json.loads(data)
            print(data_dict)
            asset_id = data_dict.get('asset_id')

            if not asset_id:
                return JsonResponse({'error': 'Pack ID is required'}, status=status.HTTP_400_BAD_REQUEST)


            files = request.FILES.getlist('asset_files')
            images = request.FILES.getlist('thumbnail_images')

            print(files)
            print(images)

            asset = Asset.objects.get(pk=asset_id)

            # Update asset fields
            asset.name = data_dict.get('name', asset.name)
            asset.base_price = data_dict.get('credits', asset.base_price)
            # category_id = data_dict.get('category_id', asset.category.id)
            # try:
            #     category = Category.objects.get(pk=category_id)
            #     asset.category = category
            # except (ValueError, Category.DoesNotExist):
            #     return JsonResponse({'error': 'Invalid category ID'}, status=400)

            is_free_str = data_dict.get('is_free',False)

            asset.is_free = is_free_str

            # Handle tags
            added_tags = data_dict.get('tags_added', [])
            print(added_tags)
            deleted_tags = data_dict.get('tags_deleted', [])
            for tag_name in added_tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                asset.tags.add(tag)
            for tag_id in deleted_tags:
                asset.tags.remove(tag_id)
            asset.save()

            #add hero images
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

            #add asset_files
            file_objects = []
            for uploaded_file in files:
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                if not file_name.endswith(".zip"):
                    file_name = os.path.splitext(file_name)[0]


                zip_file_path = os.path.join(settings.MEDIA_ROOT, f"{file_name}.zip")
                with ZipFile(zip_file_path, 'w') as zipf:
                    zipf.write(file_path, arcname=os.path.basename(file_name))

                file_name += ".zip"
                asset_type, _ = AssetType.objects.get_or_create(name=".zip")

                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_file = AssetFile.objects.create(url=file_url, asset_type=asset_type)
                file_objects.append(asset_file)

            asset.image.add(*asset_hero_images)
            asset.save()
            asset.asset_file.add(*file_objects)
            asset.save()

            #delete thumbnail images
            deleted_image_ids = data_dict.get('deleted_thumbnail_images_ids ', [])
            print(deleted_image_ids)
            for image_id in deleted_image_ids:
                try:
                    image_to_delete = Image.objects.get(pk=image_id)
                    image_to_delete.is_active = False
                    image_to_delete.save()
                    asset.image.remove(image_to_delete)
                    asset.save()
                except Image.DoesNotExist:
                    pass

            #delete asset files
            deleted_asset_files_ids = data_dict.get('deleted_asset_files_ids', [])
            print(deleted_asset_files_ids)
            for file_id in deleted_asset_files_ids:
                try:
                    file_to_delete = AssetFile.objects.get(pk=file_id)
                    file_to_delete.is_active = False
                    file_to_delete.save()
                    asset.asset_file.remove(file_to_delete)
                    asset.save()
                except AssetFile.DoesNotExist:
                    pass

            return JsonResponse({'message': 'Asset updated successfully.', 'asset_id': asset.id,'status':'true'}, status=status.HTTP_200_OK)

        except Asset.DoesNotExist:
            return JsonResponse({'error': 'Asset not found','status':'false'}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return JsonResponse({'error': 'Method not allowed','status':'false'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    


#@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_packs(request):
    u=User.objects.first()
    try:
        # packs = Pack.objects.filter(is_active=True,creator=request.user)
        packs = Pack.objects.filter(is_active=True)
        packs_data = []

        for pack in packs:
            assets = pack.assets.filter(is_active=True)

            pack_data = {
                'id': pack.id,
                'title': pack.name,
                #'creator': pack.u.id,
                'category': pack.category.name,
                'credits': pack.base_price,
                'is_free': pack.is_free,
                'is_active': pack.is_active,
                'created_at': pack.created_at,
                'updated_at': pack.updated_at,
                'tags': [{"name":tag.name,"tag_id":tag.id} for tag in pack.tags.all()],
                'hero_images': [{"image_id":image.id,"image_url":image.url} for image in pack.image.filter(is_hero=True)],
                'slider_images': [{"image_id": image.id, "image_url": image.url} for image in pack.image.filter(is_hero=False)],
                'preview_images': [{"image_id": image.id, "image_url": image.url} for image in pack.image.filter(is_preview=True)],
                'assets': []
            }

            for asset in assets:
                asset_data = {
                    'id': asset.id,
                    'name': asset.name,
                    'category': asset.category.name,
                    'credits': asset.base_price,
                    'is_free': asset.is_free,
                    'is_active': asset.is_active,
                    'created_at': asset.created_at,
                    'updated_at': asset.updated_at,
                    'tags': [{"tag_id":tag.id,"tag_name":tag.name} for tag in asset.tags.all()],
                    'images': [{"image_id":img.id,"image_url":img.url} for img in asset.image.all()],
                    'asset_file':[{"file_id":file.id,"file_url":file.url} for file in asset.asset_file.all()]
                }
                pack_data['assets'].append(asset_data)

            packs_data.append(pack_data)

        return JsonResponse({'packs': packs_data,'status':'true'}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_packs_by_title_or_tag(request):
    try:
        query = request.GET.get('query', '')
        # packs = Pack.objects.filter(is_active=True,creator=request.user)
        packs = Pack.objects.filter(is_active=True)

        if query:
            packs = packs.filter(Q(name__icontains=query) | Q(tags__name__icontains=query))

        u = User.objects.first()
        packs_data = []

        for pack in packs:
            assets = pack.assets.all()

            pack_data = {
                'id': pack.id,
                'title': pack.name,
                'category': pack.category.name,
                'credits': pack.base_price,
                'is_free': pack.is_free,
                'is_active': pack.is_active,
                'created_at': pack.created_at,
                'updated_at': pack.updated_at,
                'tags': [{"tag_id":tag.id,"tag_name":tag.name} for tag in pack.tags.all()],
                'hero_images': [{"image_id":image.id,"image_url":image.url} for image in pack.image.filter(is_hero=True)],
                'slider_images': [{"image_id": image.id, "image_url": image.url} for image in pack.image.filter(is_hero=False)],
                'preview_images': [{"image_id": image.id, "image_url": image.url} for image in pack.image.filter(is_preview=True)],
                'assets': []
            }

            for asset in assets:
                asset_data = {
                    'id': asset.id,
                    'name': asset.name,
                    'category': asset.category.name,
                    'credits': asset.base_price,
                    'is_free': asset.is_free,
                    'is_active': asset.is_active,
                    'created_at': asset.created_at,
                    'updated_at': asset.updated_at,
                    'tags': [{"tag_id":tag.id,"tag_name":tag.name} for tag in asset.tags.all()],
                    'images': [{"img_id":img.id,"img_url":img.url} for img in asset.image.all()],
                    'asset_file': [{"file_id":file.id,"file_url":file.url} for file in asset.asset_file.all()]
                }
                pack_data['assets'].append(asset_data)

            packs_data.append(pack_data)

        return JsonResponse({'packs': packs_data,'status':'true'}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_assets_by_title_and_tag(request):
    query = request.GET.get('query', '')

  
    all_assets = Asset.objects.filter(
        Q(name__icontains=query) | Q(tags__name__icontains=query)
    ).distinct()
    u=User.objects.first()
    #assets=all_assets.filter(is_active=True,creator=request.user.id)
    assets = all_assets.filter(is_active=True)

    assets_data = []
    for asset in assets:
        asset_data = {
            'id': asset.id,
            'name': asset.name,
            'category': asset.category.name,
            'credits': asset.base_price,
            'is_free': asset.is_free,
            'is_active': asset.is_active,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at,
            'tags': [{"tag_id":tag.id,"tag_name":tag.name} for tag in asset.tags.all()],
            'images': [{"img_id":img.id,"img_url":img.url} for img in asset.image.all()],
            'asset_file': [{"file_id":file.id,"file_url":file.url} for file in asset.asset_file.all()]
        }
        assets_data.append(asset_data)

    return JsonResponse({'assets': assets_data,'status':'true'},status=status.HTTP_200_OK)


#@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_product(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        pack_id = request.data.get('pack_id')


        if not pack_id:
            return JsonResponse({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = Pack.objects.get(id=pack_id)
        product.is_active = False
        product.save()
        return JsonResponse({"message": "Product soft deleted successfully",'status':'true'}, status=status.HTTP_204_NO_CONTENT)

    except Pack.DoesNotExist:
        return JsonResponse({"error": "Product not found",'status':'false'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_asset(request):
    try:
        asset_id=request.data.get("asset_id")
        asset = Asset.objects.get(id=asset_id)
        asset.is_active= False
        asset.save()
        return JsonResponse({"message": "Asset soft deleted successfully",'status':'true'},status=status.HTTP_204_NO_CONTENT)
    except Pack.DoesNotExist:
        return JsonResponse({"error": "Asset not found",'status':'false'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_pack(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = request.data.get('data')
        data_dict = json.loads(data)
        print(data_dict)
        pack_id = data_dict.get('pack_id')

        if not pack_id:
            return JsonResponse({'error': 'Pack ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        pack = Pack.objects.get(pk=pack_id)

        pack.name= data_dict.get('name', pack.name)
        pack.base_price = data_dict.get('credits', pack.base_price)

        # category_id = data_dict.get('category_id', pack.category.id)
        # category = Category.objects.get(pk=category_id)
        # pack.category = category
        is_free= data_dict.get('is_free', False)
        pack.is_free=is_free

        #add assets
        asset_ids = data_dict.get('asset_ids', [])
        print(asset_ids)
        for asset_id in asset_ids:
            try:
                asset = Asset.objects.get(id=int(asset_id))
                pack.assets.add(asset)
            except Asset.DoesNotExist:
                pass
        pack.save()


        #delete assets
        deleted_asset_ids = data_dict.get('deleted_asset_ids', [])
        print(deleted_asset_ids)
        for asset_id in deleted_asset_ids:
            try:
                asset_to_delete = Asset.objects.get(pk=asset_id)
                pack.assets.remove(asset_to_delete)
            except Asset.DoesNotExist:
                pass
        pack.save()

        #add tags
        added_tags = data_dict.get('tags_added', [])
        deleted_tags = data_dict.get('tags_deleted', [])
        print(deleted_tags)

        for tag_name in added_tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            pack.tags.add(tag)
        pack.save()

        #delete tags
        for tag_id in deleted_tags:
            pack.tags.remove(tag_id)
        pack.save()

        #add hero images
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
            asset_file, _ = Image.objects.get_or_create(url=file_url)
            pack_image_objects.append(asset_file)

            pack.image.add(*pack_image_objects)
            pack.save()

            #add preview images
            preview_images = request.FILES.getlist('preview_images')
            preview_images_objects=[]
            for uploaded_file in preview_images:
                file_name = generate_unique_filename(uploaded_file.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                image, _ = Image.objects.get_or_create(url=file_url)
                image.is_preview = True
                image.save()
                preview_images_objects.append(image)
            pack.image.add(*preview_images_objects)
            pack.save()


            #add pack slider images
            pack_slider_images = []
            slider_images = request.FILES.getlist('pack_slider_images')
            for slider_image in slider_images:
                file_name = generate_unique_filename(slider_image.name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in slider_image.chunks():
                        destination.write(chunk)
                file_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))
                asset_image = Image.objects.create(url=file_url)
                asset_image.is_hero = False
                asset_image.save()
                pack_slider_images.append(asset_image)
            pack.image.add(*pack_slider_images)
            pack.save()

            #delete images
            deleted_image_ids = data_dict.get('deleted_image_ids', [])
            for image_id in deleted_image_ids:
                try:
                    image_to_delete = Image.objects.get(pk=image_id)
                    image_to_delete.is_active=False
                    image_to_delete.save()
                    pack.image.remove(image_to_delete)
                    pack.save()
                except Image.DoesNotExist:
                    pass

            #delete assets
            deleted_asset_ids = data_dict.get('deleted_asset_ids', [])
            print(deleted_asset_ids)
            for asset_id in deleted_asset_ids:
                try:
                    asset_to_delete = Asset.objects.get(pk=asset_id)
                    pack.assets.remove(asset_to_delete)
                except Asset.DoesNotExist:
                    pass


        total_assets = pack.assets.count()
        pack.total_assets = total_assets
        pack.save()

        no_of_styles=data_dict.get('no_of_styles')
        pack.no_of_items=no_of_styles
        pack.save()


        return JsonResponse({'message': 'Pack updated successfully', 'pack_id': pack.id,'status':'true'},status=status.HTTP_200_OK)

    except Pack.DoesNotExist:
        return JsonResponse({'error': 'Pack not found','status':'false'}, status=status.HTTP_404_NOT_FOUND)

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#@permission_classes([IsAuthenticated])
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



#@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_assets(request):
    if request.method == 'GET':
        # assets=Asset.objects.filter(is_active=True,creator=request.user.id)
        assets = Asset.objects.filter(is_active=True)
        u=User.objects.first()
        all_assets=[]
        for asset in assets:
            data={
                "id":asset.id,
                "name":asset.name,
                "category":asset.category.name,
                "credits":asset.base_price,
                "hero_images":[{"image_id":image.id,"image_url":image.url } for image in asset.image.all()],
                "asset_files":[{"file_id":file.id,"file_url":file.url} for file in asset.asset_file.all()],
                "tags":[{"tag_id":tag.id,"tag_name":tag.name} for tag in asset.tags.all()]
                
            }
            all_assets.append(data)
        return JsonResponse({'all_assets':all_assets,'status':'true'}, status=status.HTTP_200_OK)













