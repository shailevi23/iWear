from django.db import migrations, transaction
from users.models import Gender, Location
from iWear.resources.genders import GENDERS_LIST
from iWear.resources.locations import LOCATION_LIST


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_gender_data(apps, schema_editor):
        with transaction.atomic():
            for gender in GENDERS_LIST:
                Gender(title=gender).save()

    def generate_locations_data(apps, schema_editor):
        with transaction.atomic():
            for location in LOCATION_LIST:
                Location(title=location).save()

    operations = [
        migrations.RunPython(generate_gender_data),
        migrations.RunPython(generate_locations_data),
    ]
