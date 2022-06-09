from products.models import Product
from analytics.models import Pixel
from django.conf import settings

def header_data(request):
    products = Product.objects.all()
    data = {}
    data["RAZORPAY_API_KEY"] = getattr(settings,"RAZORPAY_API_KEY")
    try:
        data["fb_pixel"] = Pixel.objects.filter(name="fb_pixel").first().pixel_id
        data["google_tag_manager"] = Pixel.objects.filter(name="google_tag_manager").first().pixel_id
    except:
        pass
    try: 
        for x in products:
            title = x.title.replace(' ','_')
            if (title in data.keys()):
                data[title].append(x)
            else:
                data[title] = [x]
        data["products"] = products
        data["haircare"] = products.filter(category="haircare")
        data["facecare"] = products.filter(category="facecare")
        data["bodycare"] = products.filter(category="bodycare")
    except:
        data = {}
    try:
        hair_trending = Product.objects.order_bytrending(products.filter(category="haircare"))
        face_trending = Product.objects.order_bytrending(products.filter(category="facecare"))
        body_trending = Product.objects.order_bytrending(products.filter(category="bodycare"))
        data["hair_trending"] = hair_trending[:min(5,len(hair_trending)-1)]
        data["face_trending"] = face_trending[:min(5,len(face_trending)-1)]
        data["body_trending"] = body_trending[:min(5,len(body_trending)-1)]
    except:
        pass
    return data