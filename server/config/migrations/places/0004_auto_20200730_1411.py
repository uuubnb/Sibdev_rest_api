from django.db import migrations
from apps.places.models.data import data


class Migration(migrations.Migration):

    def get_ingredient_names(apps, schema_editor):
        Ingredient = apps.get_model('places', 'Ingredient')

        for i in range(len(data)):
            Ingredient.objects.create(name=data[i][0], calories=data[i][1])

    dependencies = [
        ('places', '0003_auto_20200730_1408'),
    ]

    operations = [
        migrations.RunPython(get_ingredient_names),
    ]
