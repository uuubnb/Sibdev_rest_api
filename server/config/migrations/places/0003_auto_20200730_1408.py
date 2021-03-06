# Generated by Django 3.0.8 on 2020-07-30 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20200726_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Название ингридиента',
                'verbose_name_plural': 'Названия ингридиентов',
            },
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Название заведения', 'verbose_name_plural': 'Названия заведений'},
        ),
        migrations.AlterField(
            model_name='place',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('price', models.IntegerField(default=0)),
                ('total_calories', models.IntegerField(default=0)),
                ('ingredients', models.ManyToManyField(to='places.Ingredient')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place')),
            ],
            options={
                'verbose_name': 'Название блюда',
                'verbose_name_plural': 'Названия блюд',
            },
        ),
    ]
