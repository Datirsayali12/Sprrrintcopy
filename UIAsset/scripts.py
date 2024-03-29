from django.contrib.auth import get_user_model
from django.utils import timezone
from UIAsset.models import *
from django.db.models.functions import Upper
from accounts.models import *
from django.db.models import Count,Sum

def run():
    User = get_user_model()

    c = Category.objects.first()
    s = Subcategory.objects.first()
    pt = ProductType.objects.first()
    t = Tag.objects.get(id=1)
    at=AssetType.objects.first()
   
    p = Pack.objects.create(
        title="3d human product16",
        creator=User.objects.first(),
        category=c,
        subcategory=s,
        product_type=pt,
        created_at=timezone.now(),
        updated_at=timezone.now(),
        is_free=True,
    )
   
    p.tag.add(t)

    print(p)
   

    f = AssetFile.objects.create(
    url='https://www.example.com/asset1',  
    is_hero_img=True,
    asset_type=at,
    updated_at=timezone.now(),
    created_at=timezone.now()
    )

   
    assets_data = [
        {
            'name': 'Asset1',
            'is_free': True,
            'credits': 0,
        },
        {
            'name': 'Asset2',
            'is_free': False,
            'credits': 0,
        },
    ]

    
    assettag = AssetTag.objects.first()

    for asset_data in assets_data:
        a = Asset.objects.create(
        pack=p,
        creator=User.objects.first(),
        created_at=timezone.now(),
        updated_at=timezone.now(),
        **asset_data
    )
    a.tag.add(assettag)
    a.asset.set([f])
        # tag=Tag.objects.all()
        # l=[i.name for i in tag]
        # for j in l:
        #     t,_=Tag.objects.get_or_create(name=j)
        #     p.tag.add(t)
    


    t,_=Tag.objects.get_or_create(name="new tag")
    p.tag.add(t)

 

    total_assets = Asset.objects.filter(pack=p).count()

    total_credits = Asset.objects.filter(pack=p).aggregate(total_credits=Sum('credits'))['total_credits'] or 0
    p.is_free = total_credits == 0
    print(total_assets)
    print(total_credits)
        
    p.no_of_items = total_assets
    p.credits = total_credits
    p.save()



    




    



def update1():
    p=Pack.objects.all()
    p.update(
        title="new product"

    )
    # p=Product.objects.filter()
    # p.update(
    #     title="new product"

    # )
    #  p=Product.objects.first()
    #     >>> p.delete()
    #     (2, {'UIAsset.Product_tag': 1, 'UIAsset.Product': 1})
    #     >>> 

#     >>> p=Product.objects.all()
# >>> p=Product.objects.first()
# >>> p.title="human 3d pack"
    
#product is present or not 
    # >>> p=Product.objects.filter(id=2) 
    # >>> p.exists()
    #  True

#  p=Product.objects.filter(id=2,title__startswith="3d pack") 
#     # >>> p.exists()
#     #  True
#>> p=Product.objects.filter(credits__in=[20,10,30]) 
    

# >>> p=Product.objects.exclude(credits__in=[20,10,30]) 
# >>> p
# <QuerySet []>
# >>> where not clause
    
# <QuerySet []>
# >>> p=Product.objects.filter(credits__gte=20) 
# >>> p
# <QuerySet [<Product: new product>, <Product: new product>, <Product: new product>, <Product: new product>, <Product: new product>]>
# >>> 
#>>> p=Product.objects.filter(credits__range=(20,50)) 
# p=Product.objects.order_by('title')  
#p=Product.objects.order_by('title').reverse() descending order   
# p=Product.objects.order_by('-title')  descending order
#p=Product.objects.order_by(Lower('title'))  because of case sensitive make it lower and then arrange
    
#add this in model for default ordering
# class Meta:
#     ordering=[Lower('name')]

#> p=Product.objects.filter(tag__name__startswith='p')  for foreign key referncce filter

#for date time filed like first and last we can use earlist
#  p=Product.objects.earliest('created_at')    ascending order
    
#p=Product.objects.latest('created_at')    descending order
    
#p=Product.objects.only('tag')       to get only one column data
    
#*******************values***************************************************

# >>> f=Product.objects.values('title').first()  get first object title value
# >>> f
# {'title': 'new product'}
# >>>

# f=Product.objects.values('title','created_at')  get two columns ,get particular columns from database
    
# a=Asset.objects.filter(product=p).values('credits','asset_type__type')  get values by foreign key of asset_type
    
#a=Asset.objects.filter(product=p).values('credits') 
    


#***************************************values_list***************************************
#similar like values only difference that returns tuples    
   # >>> f=Product.objects.values_list('title')   
    #f=Product.objects.values_list('title',flat=True)  give without tuple   

#***************************aggregate**************************************
    #from django.db.models import Count,Sum
   # p=Product.objects.aggregate(total=Count('id')) 
    #op:{'total': 16}
    #a=Asset.objects.filter(product__title=n).aggregate(total=Avg('credits')) 
    #a=Asset.objects.filter(product__title=n).aggregate(total=Sum('credits')) 
    #>>> p=Product.objects.aggregate(min=Min('credits')) 
    #>>> p=Product.objects.aggregate(max=Max('credits')) 
    #>>> p=Product.objects.aggregate(min=Max('credits'),max=Max('credits'),sum,avg) 

    # >>> a=Asset.objects.filter(product__title="new product") 
    # >>> a
    # <QuerySet [<Asset: Asset object (1)>, <Asset: Asset object (3)>]>
    # >>> a
    # <QuerySet [<Asset: Asset object (1)>, <Asset: Asset object (3)>]>
    # >>> a.aggregate(min=Min('credits')) 
    # {'min': 20}


#*************************annotate************************************
    #for inner values condition
    #p=Product.objects.annotate(len_name=Length('title')).filter(len_name__gt=3) 



       
    

