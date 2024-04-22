import requests


def get_tags():
    url = 'http://127.0.0.1:8000/Dashboard/get-tags/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    return None  


def get_pack_data():
    url = 'http://127.0.0.1:8000/Dashboard/get-all-packs/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    return None  



def get_existing():
    url = 'http://127.0.0.1:8000/Dashboard/get-selected-existing/'

  
    data = {
        "asset_ids": [1]  
    }

    response = requests.post(url, json=data)

    return response.json()

def get_pack_by_title():
    url="http://127.0.0.1:8000/Dashboard/get-packs-by-title-or-tag/?query=pa"


    response = requests.get(url)

    return response.json()


def delete_asset():
    url="http://127.0.0.1:8000/Dashboard/delete-asset/1/"


    response = requests.delete(url)

    return response.json()


def delete_pack():
    url="http://127.0.0.1:8000/Dashboard/delete-product/1/"


    response = requests.delete(url)

    return response.json()

def delete_assets():
    url = "http://127.0.0.1:8000/Dashboard/delete-asset/1/"
    response = requests.delete(url)
    if response.status_code == 200:
        return {"message": "Asset deleted successfully"}
    elif response.status_code == 404:
        return {"error": "Asset not found"}
    elif response.status_code == 500:
        return {"error": "Internal server error"}
    else:
        return {"error": "Unexpected error"}
    



def upload_asset():
    url = 'http://127.0.0.1:8000/Dashboard/upload-asset/'

    # Define the JSON data
    data = {
        "data": json.dumps({
            "name": "Asset17",
            "tags": ["tag3", "tag2"],
            "category_id": 1,
            "credits": 10,
            "is_free": True  # 'true' should be boolean, not string
        })
    }

    # Define the files to be uploaded
    files = [
        ('asset_files', ('file1.png', open('C:\\Users\\Lenovo\\Downloads\\file1.png', 'rb'), 'image/png')),
        ('thumbnail_images', ('file1.png', open('C:\\Users\\Lenovo\\Downloads\\file1.png', 'rb'), 'image/png'))
    ]

    # Send the POST request
    response = requests.post(url, data=data, files=files)

    # Return the JSON response
    return response.json()


import json


def upload_pack():
    url = 'http://127.0.0.1:8000/Dashboard/upload-pack/'

    data = {
        "data": json.dumps({
        "name": "pack23",
        "category_id": 1,
        'credits': 100,
        'tags': ['tag1', 'tag2'],
        'is_free': False,
        'asset_ids': [1, 2],
            })
    }

    
    files = [
        ('hero_images',('file1.png',open('C:\\Users\\Lenovo\\Downloads\\file1.png','rb'),'image/png')),
        ('hero_images',('file1.png',open('C:\\Users\\Lenovo\\Downloads\\file1.png','rb'),'image/png'))
    ]
    response = requests.post(url, data=data, files=files)

   
    return response.status_code, response.json()


#********************************************Update Assets and pack***********************************
def update_asset():
    url = 'http://127.0.0.1:8000/Dashboard/update-asset/2/'

    data = {
        "data":json.dumps( {
            "name": "Updated Asset Name",
            "credits": 20,
            "is_free": True,
            "tags_added": ["new_tag1", "new_tag2"],
            "tags_deleted": [1,2],
            "deleted_thumbnail_images_ids ": [60,61],
            "deleted_asset_files_ids": [54,55]
        })
    }

    files = [
        ('asset_files', ('file1.png',open('C:\\Users\\Lenovo\\Downloads\\file1.png','rb'),'image/png')),
        ('thumbnail_images', ('file1.png',open('C:\\Users\\Lenovo\\Downloads\\file1.png','rb'),'image/png')),
    ]

    response = requests.put(url, data=data,files=files)

    return response.json()





def update_pack():
    url = 'http://127.0.0.1:8000/Dashboard/update-pack/2/'

    data = {
         "data":json.dumps({"name": "pack27",
         "credits": 10,
         "asset_ids": [1, 2],
         "tags_added": ["tag125"],
         "tags_deleted": [1, 2, 3,7],
         "deleted_image_ids": [48, 49],
         "is_free": True,
         "deleted_asset_ids": [1]

     })
    }

    
    files = [
        ('hero_images',('file1.png',open('C:\\Users\\Lenovo\\Downloads\\file1.png','rb'),'image/png')),
        ('hero_images',('file1.png',open('C:\\Users\\Lenovo\\Downloads\\file1.png','rb'),'image/png'))
    ]
    response = requests.put(url, data=data,files=files)

    print(response)
    return response.status_code, response.json()



def create_from_existing():
    url="http://127.0.0.1:8000/Dashboard/create-from-existing/"

    data = {
      "data": json.dumps({
      "name": "New Asset Name",
      "asset_id": 1,
      "credits": 100,
      "is_free": True
       })
    }

    response=requests.post(url,data=data)
    return response.json()