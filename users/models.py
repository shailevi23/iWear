from clothing.models import ClothingItem
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name,
                    last_name, birth_date, password,
                    **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        if not first_name:
            raise ValueError('You must provide a first name')

        if not last_name:
            raise ValueError('You must provide a last name')

        if not birth_date:
            raise ValueError('You must provide a birth date')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, birth_date=birth_date,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name,
                         last_name, birth_date, password,
                         **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if not other_fields.get('is_staff'):
            raise ValueError('superuser must be assigned to is_staff=True')

        if not other_fields.get('is_superuser'):
            raise ValueError('superuser must be assigned to is_superuser=True')

        return self.create_user(email, first_name,
                                last_name, birth_date, password,
                                **other_fields)

class Gender(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Location(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='location')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True, related_name='gender')
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    reader_id = models.CharField(max_length=10000, unique=True)
    image_url = models.TextField(blank=True, default='/static/img/default_profile_img.png')
    date_joined = models.DateField(default=timezone.now)

    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date']

    def __str__(self):
        return f"{self.email}"

    @property
    def all_items(self):
        return ClothingItem.objects.filter(owner=self)

    @property
    def number_of_items_in_closet(self):
        all_items = self.all_items
        return all_items.count()
    
    def get_total_worn_events(self, category):
        total_worn_events = 0
        items = ClothingItem.objects.filter(owner=self, category=category)
        for curr_item in items:
            total_worn_events = total_worn_events  + curr_item.total_worn_events
        return total_worn_events
