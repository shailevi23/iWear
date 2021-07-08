from django.db import migrations, transaction
from users.models import Gender
from iWear.resources.genders import GENDERS_LIST


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_gender_data(apps, schema_editor):
        with transaction.atomic():
            for gender in GENDERS_LIST:
                Gender(title=gender).save()

    operations = [
        migrations.RunPython(generate_gender_data),
    ]
