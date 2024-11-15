from django.shortcuts import render
from .models import Categories,Product,ProductImage
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


# Create your views here.
def home(request):
    catogery=Categories.objects.all()
    products=Product.objects.all()
    product = None
    if 'product_id' in request.GET:
        product_id = request.GET['product_id']
        product = get_object_or_404(Product, id=product_id)
    context={
        'catogery':catogery,
        'products':products,
         'product': product,
    }
    return render(request,'products/home.html',context)


def products(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'products/products.html',context)

def products_detail(request,id):
    product = get_object_or_404(Product, id=id)
    context={
        'product':product
    }
    return render(request,'products/product_detail.html',context)


def brand_products(request, brand_name):
    products = Product.objects.filter(category__brand_name=brand_name)
    
    context = {
        'products': products,
        'brand_name': brand_name
    }
    
    return render(request, 'products/brand_products.html', context)

def catogery(request):
    print('hi')
    error_message = None
    modal_open = False
    categories = Categories.objects.all()
    if request.method=='POST':
        image=request.FILES.get('catogeryimage')
        name=request.POST.get('name')
        status=request.POST.get('status')
        
        if Categories.objects.filter(brand_name=name).exists():
             error_message = "Category with this name already exists!"
             modal_open = True
        else:
            catogery=Categories.objects.create(brand_name=name,active=status,image=image)
            return redirect('products:catogery')
    context={
       'categories': categories,
       'error_message':error_message,
       'modal_open':modal_open 
    }
    return render(request,'products/catogery.html',context)
def edit_catogery(request,id):
    catogery=get_object_or_404(Categories,id=id)
    
    if request.method=='POST':
        name=request.POST.get('brand_name')
        active=request.POST.get('active') 
        image=request.FILES.get('image')
        catogery.brand_name=name
        catogery.active=active
        if image:
            catogery.image=image
        
        catogery.save()
        print('catogery:',catogery)
        return redirect('products:catogery')
      
    return render(request,'admin1/catogery.html')
def catogerylist(request,id):
    if request.method=='POST':
        catogery=get_object_or_404(Categories,id=id)
        if catogery.status=='listed':
            catogery.status='dislisted'
        else:
            catogery.status='listed'
        catogery.save()
        return redirect('catogery')
    
def products_admin(request):
    categories = Categories.objects.all()
    products=Product.objects.all()
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        size=request.POST.get('size')
        price=request.POST.get('price')
        stock=request.POST.get('stock')
        description=request.POST.get('description')
        images=request.FILES.getlist('images')
        category_id = request.POST.get('category')  
        category = Categories.objects.get(id=category_id) if category_id else None
        products=Product.objects.create(name=product_name,description=description,size=size,price=price,stock=stock,category=category)
        if 'images' in request.FILES:
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=products, image=image)
            return redirect('products:products_admin')
    context={
        'categories':categories,
        'products':products
    } 
    return render(request,'products/products_admin.html',context)

def productlist(request,id):
    if request.method=='POST':
        products=get_object_or_404(Product,id=id)
        if products.status=='listed':
            products.status='dislisted'
        else:
            products.status='listed'
        products.save()
        return redirect('products:products_admin')
    
