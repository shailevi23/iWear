from django.db import migrations, transaction
from clothing.models import ClothCategory
from iWear.resources.clothCategories import CLOTH_CATEGORIES_LIST


class Migration(migrations.Migration):
    dependencies = [
        ('clothing', '0002_clothingitem_owner'),
    ]

    def generate_clothcategories_data(apps, schema_editor):   
        with transaction.atomic():
            for category in CLOTH_CATEGORIES_LIST:
                ClothCategory(category_name=category).save()

    operations = [
        migrations.RunPython(generate_clothcategories_data),
    ]
    