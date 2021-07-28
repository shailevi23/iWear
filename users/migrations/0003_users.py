from django.db import migrations, transaction
from users.models import Gender, User
from iWear.resources.names import FIRST_NAME_LIST, LAST_NAME_LIST
from iWear.resources.images import PROFILE_IMAGE_URL_LIST
import random


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_test_data_gender'),
    ]

    def generate_user_data(apps, schema_editor):
        password = "iWear2021"

        users_test_data = [
            ('iWear@iWear.com', 'Amit', 'iWear', '1994-04-26', 5, "https://user-images.githubusercontent.com/58184521/121235257-54058280-c89d-11eb-9613-1590a2396d57.png"),
            ('TestUser@iWear.com', 'Amit', 'Test', '1994-04-26', 6, "https://user-images.githubusercontent.com/58184521/121235257-54058280-c89d-11eb-9613-1590a2396d57.png"),
            ('Amit@iWear.com', 'Amit', 'Aharoni', '1994-04-26', 7, "https://scontent.fsdv1-2.fna.fbcdn.net/v/t31.18172-8/20248083_10203213989907988_3630261739891709060_o.jpg?_nc_cat=111&ccb=1-3&_nc_sid=09cbfe&_nc_ohc=XolrSsZMNU4AX-Ore7y&tn=hR76xO3MAtE8NAF4&_nc_ht=scontent.fsdv1-2.fna&oh=4c4688e57b432feaf074c91dd1e10c7c&oe=60EC4AE7"),
            ('Dror@iWear.com', 'Dror', 'Margalit', '1990-01-01', 8, "https://www.prolink.co.il/wp-content/uploads/2019/01/18_20160914_1693791918-1.jpg"),
            ('Liran@iWear.com', 'Liran', 'Chaim-Jan', '1993-03-18', 9, "https://scontent.fsdv1-2.fna.fbcdn.net/v/t1.6435-9/70895053_10219609279239594_2087406298298580992_n.jpg?_nc_cat=103&ccb=1-3&_nc_sid=09cbfe&_nc_ohc=SQkW0LvLWccAX8KOhV6&_nc_ht=scontent.fsdv1-2.fna&oh=73376bd7e58d6a55bfdd5d8be0fbb723&oe=60EB9499"),
        ]

        for i in range(10, 20):
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

    operations = [
        migrations.RunPython(generate_user_data),
        migrations.RunPython(add_user_Gender),
    ]
