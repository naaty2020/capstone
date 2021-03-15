from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class VendorType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Vendor(User):
    address = models.CharField(max_length=60, null=True)
    logo = models.URLField(default="https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty-300x240.jpg")
    cover = models.URLField(default="https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty-300x240.jpg")
    vendor_type = models.ForeignKey(VendorType, null=True, on_delete=models.CASCADE, related_name="vendors")
    about = models.TextField(null=True)
    moto = models.TextField(null=True)
    verified = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "logo": self.logo,
            "about": self.about
        }

    def __str__(self):
        return self.username

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribed")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="subscribers")

    class Meta:
        unique_together = ("user", "vendor")

    def __str__(self):
        return f"{self.user} subscribed to {self.vendor}"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=50)
    seen_count = models.PositiveIntegerField(default=0)
    image = models.URLField(default="https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty-300x240.jpg")    
    upcoming = models.BooleanField(default=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name="items")
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "vendor": self.vendor.username,
            "vendor_id": self.vendor.id,
            "vendor_logo": self.vendor.logo,
            "name": self.name,
            "seen_count": self.seen_count,
            "image": self.image,
            "upcoming": self.upcoming,
            "category": self.category.name,
            "price": self.price,
            "description": self.description,
            "date_created": self.date_created
        }    

    def __str__(self):
        return self.name

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment