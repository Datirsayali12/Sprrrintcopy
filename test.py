import requests

def get_tags():
    url = 'http://127.0.0.1:8000/Dashboard/get-tags/'  # Update with your actual URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad status codes
        return response.json()  # Assuming response is JSON
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    return None  


def get_pack_data():
    url = 'http://127.0.0.1:8000/Dashboard/get-pack-details/'  # Update with your actual URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad status codes
        return response.json()  # Assuming response is JSON
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    return None  


import requests

def upload_asset():
    url = "http://127.0.0.1:8000/Dashboard/upload-asset/"

    payload = {
        'name': 'Asset19',
        'credits': '20',
        'is_active': 'True',
        'tags': ['tag3', 'tag2'],  
        'category_id': '1'
    }

    files = [
        ('files', ('WhatsApp Image 2024-04-01 at 11,19,29 PM-photoaidcom-cropped (1).jpeg', open('C:\\Users\\sayal\\Downloads\\WhatsApp Image 2024-04-01 at 11,19,29 PM-photoaidcom-cropped (1).jpeg', 'rb'), 'image/jpeg')),
        ('image', ('fotor-20240401232828.png', open('C:\\Users\\sayal\\Downloads\\fotor-20240401232828.png', 'rb'), 'image/png'))
    ]
    
    headers = {
     
        'Content-Type': 'application/json'  
    }

    response = requests.post(url, headers=headers, data=payload, files=files)
    print(response)

    return response.text


def get_existing():
    url = 'http://127.0.0.1:8000/Dashboard/get-existing/'  

  
    data = {
        "asset_ids": [1]  
    }

 
    response = requests.post(url, json=data)

    return response.json()

def get_pack_by_title():
    url="http://127.0.0.1:8000/Dashboard/get-packs-by-title/"

    params={
        "title":"p"
    }

    response = requests.get(url, params=params)

    return response.json()


def delete_asset():
    url="http://127.0.0.1:8000/Dashboard/delete-asset/1/"


    response = requests.delete(url)

    return response.json()


def delete_product():
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

 
    data = {
        'name': 'Example Asset',
        'category_id': 1,  
        'credits': 10,
        'is_active': 'true',
        'tags': ['tag1', 'tag2']  
    }

   
    files=[
        ('files',('file1.txt',open('E:\\test4\\file1.txt','rb'),'text/plain')),
        ('image',('file2.txt',open('E:\\test4\\file2.txt','rb'),'text/plain')),
        
        ]


    response = requests.post(url, data=data, files=files)

    
    return response.json()





def upload_pack():
    url = 'http://127.0.0.1:8000/Dashboard/upload-pack/'

    data = {
        'title': 'Example Pack',
        'category_id': 1,
        'product_type': 'single',
        'base_price': 100,
        'discount_price': 80,
        'no_of_items': 5,
        'tags': ['tag1', 'tag2'],
        'asset_ids': [5]  
    }

    
    files = [
        ('hero_images',('WhatsApp Image 2024-04-01 at 11,19,29 PM-photoaidcom-cropped.jpeg',open('C:\\Users\\sayal\\Downloads\\WhatsApp Image 2024-04-01 at 11,19,29 PM-photoaidcom-cropped.jpeg','rb'),'image/jpeg')),
        ('hero_images',('fotor-20240401232828.png',open('C:\\Users\\sayal\\Downloads\\fotor-20240401232828.png','rb'),'image/png'))
    ]
    response = requests.post(url, data=data, files=files)

   
    return response.status_code, response.json()



def update_asset():
    url = 'http://127.0.0.1:8000/Dashboard/update-asset/2/'  

 
    data = {
        'name': 'Example1',
        'category_id': 1,  
        'credits': 10,
        'is_active': 'true',
        'tags': ['tag1', 'tag2','tag3']  
    }

   
    files=[
        ('files',('file1.txt',open('E:\\test4\\file1.txt','rb'),'text/plain')),
        ('image',('file2.txt',open('E:\\test4\\file2.txt','rb'),'text/plain')),
        
        ]


    response = requests.put(url, data=data, files=files)

    
    return response.json()





def update_pack():
    url = 'http://127.0.0.1:8000/Dashboard/update-pack/2/'

    data = {
        'title': 'Example Pack12',
        'category_id': 1,
        'product_type': 'single',
        'base_price': 100,
        'discount_price': 80,
        'no_of_items': 5,
        'tags': ['tag1', 'tag2'],
        'asset_ids': [5]  
    }

    
    files = [
        ('hero_images',('WhatsApp Image 2024-04-01 at 11,19,29 PM-photoaidcom-cropped.jpeg',open('C:\\Users\\sayal\\Downloads\\WhatsApp Image 2024-04-01 at 11,19,29 PM-photoaidcom-cropped.jpeg','rb'),'image/jpeg')),
        ('hero_images',('fotor-20240401232828.png',open('C:\\Users\\sayal\\Downloads\\fotor-20240401232828.png','rb'),'image/png'))
    ]
    response = requests.put(url, data=data, files=files)

    print(response)
    return response.status_code, response.json()
