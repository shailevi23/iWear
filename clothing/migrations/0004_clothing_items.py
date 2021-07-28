import datetime
from django.db import migrations, transaction
from users.models import User
from clothing.models import ClothCategory, ClothingItem, WornEvent
from iWear.resources.clothCategories import CLOTH_CATEGORIES_LIST
from iWear.resources.names import FIRST_NAME_LIST, LAST_NAME_LIST
from iWear.resources.images import PROFILE_IMAGE_URL_LIST, Shirt_IMAGE_URL_LIST, Skirt_IMAGE_URL_LIST, Suit_IMAGE_URL_LIST, Sweater_IMAGE_URL_LIST, Swimsuit_IMAGE_URL_LIST, Shorts_IMAGE_URL_LIST, Coat_IMAGE_URL_LIST, Jacket_IMAGE_URL_LIST, Jeans_IMAGE_URL_LIST, Hoodies_IMAGE_URL_LIST, Polo_IMAGE_URL_LIST
import random

class Migration(migrations.Migration):
    dependencies = [
        ('clothing', '0003_test_data_clothCategories'),
        ('users', '0003_users'),
    ]

    def generate_clothing_items(apps, schema_editor):
        users = User.objects.all()
        categories = ClothCategory.objects.all()
        items_counter = 1
        items_test_data = []
        
        for user in users:
            num_of_categories = random.randint(4, categories.count())
            
            for i in range(num_of_categories):
                num_of_items = random.randint(1, 4)
                num_of_items = num_of_items * 5
                curr_category_rand_num = random.randint(1, num_of_categories)
                cat = ClothCategory.objects.get(id=curr_category_rand_num)

                for j in range(num_of_items):
                    name = "item " + "#" + str(items_counter)
                    owner = user
                    category = cat
                    tag_id = items_counter

                    if(cat.category_name == "Shirt"):
                        cat_imgs_list = Shirt_IMAGE_URL_LIST 
                    elif(cat.category_name == "Skirt"):
                        cat_imgs_list = Skirt_IMAGE_URL_LIST 
                    elif(cat.category_name == "Suit"):
                        cat_imgs_list = Suit_IMAGE_URL_LIST 
                    elif(cat.category_name == "Sweater"):
                        cat_imgs_list = Sweater_IMAGE_URL_LIST 
                    elif(cat.category_name == "Swimsuit"):
                        cat_imgs_list = Swimsuit_IMAGE_URL_LIST 
                    elif(cat.category_name == "Shorts"):
                        cat_imgs_list = Shorts_IMAGE_URL_LIST 
                    elif(cat.category_name == "Coat"):
                        cat_imgs_list = Coat_IMAGE_URL_LIST 
                    elif(cat.category_name == "Jacket"):
                        cat_imgs_list = Jacket_IMAGE_URL_LIST 
                    elif(cat.category_name == "Jeans"):
                        cat_imgs_list = Jeans_IMAGE_URL_LIST 
                    elif(cat.category_name == "Hoodies"):
                        cat_imgs_list = Hoodies_IMAGE_URL_LIST 
                    elif(cat.category_name == "Polo"):
                        cat_imgs_list = Polo_IMAGE_URL_LIST 

                    image_url = random.choice(cat_imgs_list)
                    item_details = (name, owner, category, tag_id, image_url)
                    items_test_data.append(item_details)
                    items_counter += 1
                
        with transaction.atomic():
            for name, owner, category, tag_id, image_url in items_test_data:
                item = ClothingItem(name=name, owner=owner, category=category, tag_id=tag_id, image_url=image_url,)
                item.save()

    def generate_worn_events(apps, schema_editor):
        items = ClothingItem.objects.all()
        worn_events_test_data = []

        for item in items:
            num_of_worn_events = random.randint(0, 30)

            for i in range(num_of_worn_events):
                item = item
                time_stamp = str(random.randint(2000, 2021)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
                temperture = random.randint(-15, 45)

                worn_event_details = (item, time_stamp, temperture)
                worn_events_test_data.append(worn_event_details)

        with transaction.atomic():
            for item, time_stamp, temperture in worn_events_test_data:
                worn_event = WornEvent(item=item, time_stamp=time_stamp, temperture=temperture)
                worn_event.save()

    operations = [
        migrations.RunPython(generate_clothing_items),
        migrations.RunPython(generate_worn_events),
    ]

    