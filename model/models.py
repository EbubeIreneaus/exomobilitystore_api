from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
from cloudinary.models import CloudinaryField

class UserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(email=email, fullname=fullname, password=password, **extra_fields)
        return user

class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.first_name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Specification(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="specifications")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ('category', 'name')
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    feature = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.specification.name}: {self.value}"

    class Meta:
        unique_together = ('product', 'specification')

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField("products/images", transformation=[
        {'format': 'webp'}
    ])

    def __str__(self):
        return self.product.name

class Video(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='video')
    video = CloudinaryField("products/videos", resource_type="video" )

    def __str__(self):
        return self.product.name

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question







# Create your models here.
