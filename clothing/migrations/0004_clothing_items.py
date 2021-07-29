from django.db import migrations, transaction
from users.models import User
from clothing.models import ClothCategory, ClothingItem, WornEvent
from iWear.resources.images import  Shirt_IMAGE_URL_LIST, Skirt_IMAGE_URL_LIST, Suit_IMAGE_URL_LIST, Sweater_IMAGE_URL_LIST, Swimsuit_IMAGE_URL_LIST, Shorts_IMAGE_URL_LIST, Coat_IMAGE_URL_LIST, Jacket_IMAGE_URL_LIST, Jeans_IMAGE_URL_LIST, Hoodies_IMAGE_URL_LIST, Polo_IMAGE_URL_LIST
from iWear.resources.clothes import Shirt_NAMES, Skirt_NAMES, Suit_NAMES, Sweater_NAMES, Swimsuit_NAMES, Shorts_NAMES, Coat_NAMES, Jacket_NAMES, Jeans_NAMES, Hoodies_NAMES, Polo_NAMES
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
        total_cat_number = categories.count()
        for user in users:
            num_of_categories = random.randint(1, total_cat_number)

            for i in range(num_of_categories):
                num_of_items = random.randint(1, 5)
                num_of_items = num_of_items * 5
                curr_category_rand_num = random.randint(1, total_cat_number)
                cat = ClothCategory.objects.get(id=curr_category_rand_num)

                for j in range(num_of_items):
                    owner = user
                    category = cat
                    tag_id = items_counter

                    if(cat.category_name == "Shirt"):
                        cat_names_list = Shirt_NAMES
                        cat_imgs_list = Shirt_IMAGE_URL_LIST 
                    elif(cat.category_name == "Skirt"):
                        cat_names_list = Skirt_NAMES
                        cat_imgs_list = Skirt_IMAGE_URL_LIST 
                    elif(cat.category_name == "Suit"):
                        cat_names_list = Suit_NAMES
                        cat_imgs_list = Suit_IMAGE_URL_LIST 
                    elif(cat.category_name == "Sweater"):
                        cat_names_list = Sweater_NAMES 
                        cat_imgs_list = Sweater_IMAGE_URL_LIST 
                    elif(cat.category_name == "Swimsuit"):
                        cat_names_list = Swimsuit_NAMES 
                        cat_imgs_list = Swimsuit_IMAGE_URL_LIST 
                    elif(cat.category_name == "Shorts"):
                        cat_names_list = Shorts_NAMES 
                        cat_imgs_list = Shorts_IMAGE_URL_LIST 
                    elif(cat.category_name == "Coat"):
                        cat_names_list = Coat_NAMES 
                        cat_imgs_list = Coat_IMAGE_URL_LIST 
                    elif(cat.category_name == "Jacket"):
                        cat_names_list = Jacket_NAMES 
                        cat_imgs_list = Jacket_IMAGE_URL_LIST 
                    elif(cat.category_name == "Jeans"):
                        cat_names_list = Jeans_NAMES 
                        cat_imgs_list = Jeans_IMAGE_URL_LIST 
                    elif(cat.category_name == "Hoodies"):
                        cat_names_list = Hoodies_NAMES 
                        cat_imgs_list = Hoodies_IMAGE_URL_LIST 
                    elif(cat.category_name == "Polo"):
                        cat_names_list = Polo_NAMES 
                        cat_imgs_list = Polo_IMAGE_URL_LIST 


                    random_index = int(random.randint(0, len(cat_names_list)-1))
                    name = cat_names_list[random_index]
                    image_url = cat_imgs_list[random_index]
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

    