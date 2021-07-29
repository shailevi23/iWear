from django.db import migrations, transaction
from users.models import Gender, User, Location
from iWear.resources.names import FIRST_NAME_LIST, LAST_NAME_LIST
from iWear.resources.images import PROFILE_IMAGE_URL_LIST
import random


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_add_genders_locations'),
    ]

    def generate_user_data(apps, schema_editor):
        password = "iWear2021"

        users_test_data = [
            ('iWear@iWear.com', 'Amit', 'iWear', '1994-04-26', 5, "/static/img/amit.jpg"),
            ('Amit@iWear.com', 'Amit', 'Aharoni',  '1994-04-26', 6, "/static/img/amit.jpg"),
            ('Liran@iWear.com', 'Liran', 'Chaim-Jan', '1993-03-18', 7, "/static/img/liran.jpg"),
        ]

        for i in range(10, 13):
            email = "user" + str(i) + "@iWear.com"
            first_name = random.choice(FIRST_NAME_LIST)
            last_name = random.choice(LAST_NAME_LIST)
            birth_date = str(random.randint(1980, 2000)) + "-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
            reader_id = i
            image_url = random.choice(PROFILE_IMAGE_URL_LIST)

            user_details = (email, first_name, last_name, 
                birth_date, reader_id, image_url)
            users_test_data.append(user_details)

        with transaction.atomic():
            for email, first_name, last_name, birth_date, reader_id, image_url in users_test_data:
                user = User(email=email, first_name=first_name, last_name=last_name, birth_date=birth_date,
                    reader_id=reader_id, image_url=image_url,)
                user.set_password(password)
                user.save()
        
    def add_user_Gender(apps, schema_editor):
        with transaction.atomic():
            genders = Gender.objects.all()

            for user in User.objects.all():
                gender = random.choice(genders)
                user.gender = gender
                user.save()

    def add_user_Location(apps, schema_editor):
        with transaction.atomic():
            locations = Location.objects.all()

            for user in User.objects.all():
                location = random.choice(locations)
                user.location = location
                user.save()

    def add_admin_user(apps, schema_editor):
        password = "iWear2021"

        admin_data = [
            ('admin@iWear.com', 'iWear', 'Admin', Location.objects.get(title='Tel Aviv'), '1994-04-26', 0, "https://user-images.githubusercontent.com/58184521/121235257-54058280-c89d-11eb-9613-1590a2396d57.png"),
        ]

        with transaction.atomic():
            for email, first_name, last_name, location, birth_date, reader_id, image_url in admin_data:
                user = User(email=email, first_name=first_name, last_name=last_name, location=location, birth_date=birth_date,
                    reader_id=reader_id, image_url=image_url, is_superuser=True, is_staff=True)
                user.set_password(password)
                user.save()     

    operations = [
        migrations.RunPython(generate_user_data),
        migrations.RunPython(add_user_Gender),
        migrations.RunPython(add_user_Location),
        migrations.RunPython(add_admin_user),
    ]
