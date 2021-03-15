import json
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect

from .models import *

# Create your views here.
def index(request):
    items = Item.objects.all().order_by("-date_created")
    return render(request, "negade/index.html", {
        "items": items
    })

def item(request, id):
    itm = Item.objects.get(pk=id)
    if request.method == "GET":
        if request.user.id != itm.vendor.id:
            itm.seen_count += 1
            itm.save()
        v_items = itm.vendor.items.exclude(pk=id)
        c_items = itm.category.items.exclude(pk=id)
        return render(request, "negade/item.html", {
            "item": itm,
            "v_items": v_items,
            "c_items": c_items
        })
    
    elif request.method == "POST":
        c = Comments(user=request.user, comment=request.POST['text'], item=itm)
        c.save()
        return HttpResponseRedirect(reverse("item", args = (id,)))

@csrf_exempt
@login_required
def subscribe(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)    
    v = Vendor.objects.get(pk=data.get("vendor_id"))
    try:
        subscribe = Subscription(user=request.user, vendor=v)
        subscribe.save()
    except IntegrityError:
        Subscription.objects.get(user=request.user, vendor=v).delete()
    finally:        
        return JsonResponse({"message": "Successful"}, status=200)

def type_vendor(request, uname):
    typ = VendorType.objects.get(name=uname)
    vendors = Vendor.objects.filter(vendor_type=typ)
    return JsonResponse([v.serialize() for v in vendors], safe=False)

def item_json(request, id):
    item = Item.objects.get(pk=id)
    item.seen_count += 1
    item.save()
    return JsonResponse(item.serialize(), safe=False)

def trending_items(request):
    it = Item.objects.aggregate(Avg('seen_count'))
    items = Item.objects.filter(seen_count__gt=it['seen_count__avg']).order_by("-seen_count")
    return JsonResponse([item.serialize() for item in items], safe=False)

def isNew(x):
    return datetime.datetime.now().timestamp() - x['date_created'].timestamp() < 259200

def new_items(request):
    items = list(Item.objects.values().order_by("-date_created"))
    return JsonResponse(list(filter(isNew, items)), safe=False)

def all_items(request):
    items = Item.objects.all().order_by("-date_created")
    return JsonResponse([item.serialize() for item in items], safe=False)
    
def upcoming_items(request):
    items = Item.objects.filter(upcoming=True).order_by("-date_created")
    return JsonResponse([item.serialize() for item in items], safe=False)

def subscription_items(request):
    vendors = [u.vendor for u in request.user.subscribed.all()]
    ven = []
    for v in vendors:
        for item in v.items.all().order_by("-date_created"):
            ven.append(item.serialize())
    return JsonResponse(ven, safe=False)

def vendor_items(request, name):
    vendor = Vendor.objects.get(username=name)
    items = vendor.items.all()[:10]
    return JsonResponse([item.serialize() for item in items], safe=False)

def category_items(request, name):
    category = Category.objects.get(name=name)
    items = category.items.all()[:10]
    return JsonResponse([item.serialize() for item in items], safe=False)

def vendors(request):
    vendors = Vendor.objects.all()
    return render(request, "negade/vendors.html", {
        "vendors": vendors,
        "vendor_types": VendorType.objects.all()
    })

def vendor(request, id):
    vendor = Vendor.objects.get(pk=id)
    subs = [s.user for s in vendor.subscribers.all()]
    return render(request, "negade/vendor.html", {
        "vendor": vendor,
        "subs": subs
    })

def search(request):
    if request.method == "GET":
        value = request.GET["value"]
        items = Item.objects.filter(name__icontains=value)
        vendors = Vendor.objects.filter(username__icontains=value)
        return render(request, "negade/search.html", {
            "items": items,
            "vendors": vendors
        })
    else:
        return render(request, "negade/error.html", {
            "message": "Unauthorized access"
        })

def verified(request, ver):
    vendors = Vendor.objects.filter(verified=True if ver == 0 else False)
    return JsonResponse([v.serialize() for v in vendors], safe=False)

def subscribed(request, sub):
    vendors = [u.vendor for u in request.user.subscribed.all()]
    if sub == 1:
        ven = vendors
        vendors = [v for v in Vendor.objects.all() if v not in ven]
    return JsonResponse([v.serialize() for v in vendors], safe=False)

@login_required
def vendor_home(request, name):
    return render(request, "negade/vendor_home.html", {
        "vendor": Vendor.objects.get(username=name)
    })

@login_required
def edit_page(request, id):
    v = Vendor.objects.get(pk=id)
    if request.method == "GET":
        return render(request, "negade/edit_page.html", {
            "vendor_types": VendorType.objects.all(),
            "vendor": v
        })
    
    elif request.method == "POST":        
        v.username = request.POST["name"]
        v.email = request.POST["email"]
        v.address = request.POST["address"]
        v.vendor_type = VendorType.objects.get(pk=request.POST["vendor_type"])
        v.moto = request.POST["moto"]
        v.about = request.POST["about"]
        v.logo = request.POST["logo"]
        v.cover = request.POST["cover"]
        v.save()
        return HttpResponseRedirect(reverse("vendor_home", args=(request.POST["name"],)))

@login_required
def add_item(request):
    if request.method == "GET":
        return render(request, "negade/add_item.html", {
            "categories": Category.objects.all()
        })

    elif request.method == "POST":
        nam = request.POST["name"]
        cat = Category.objects.get(pk=request.POST["category"])
        des = request.POST["description"]
        pri = request.POST["price"]
        img = request.POST["img"]
        upc = True if request.POST.getlist("upcoming") == ["1"] else False
        ven = Vendor.objects.get(username=request.user.username)
        i = Item(name=nam, vendor=ven, image=img, upcoming=upc, category=cat, price=pri, description=des)
        i.save()
        return HttpResponseRedirect(reverse("vendor_home", args=(ven.username,)))

@login_required
def edit_item(request, id):
    i = Item.objects.get(pk=id)
    if request.method == "GET":
        return render(request, "negade/edit_item.html", {
            "item": i,
            "categories": Category.objects.all()
        })

    elif request.method == "POST":
        if 'edit' in request.POST:
            i.name = request.POST["name"]
            i.category = Category.objects.get(pk=request.POST["category"])
            i.description = request.POST["description"]
            i.price = request.POST["price"]
            i.image = request.POST["img"]
            i.upcoming = True if request.POST.getlist("upcoming") == ["1"] else False
            i.save()
            return HttpResponseRedirect(reverse("item", args=(id,)))
        elif 'delete' in request.POST:
            i.delete()
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "negade/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "negade/login.html")

def vendor_login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None and user.is_vendor:
            login(request, user)
            return HttpResponseRedirect(reverse("vendor_home", args=(username,)))
        else:
            return render(request, "negade/vendor_login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "negade/vendor_login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "negade/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "negade/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "negade/register.html")

def vendor_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "negade/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = Vendor.objects.create_user(username, email, password)
            user.is_vendor = True
            user.save()
        except IntegrityError:
            return render(request, "negade/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("vendor_home", args=(username,)))
    else:
        return render(request, "negade/vendor_register.html")