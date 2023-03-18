# Generated by Django 3.2.16 on 2023-03-18 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_app', '0015_remove_recipe_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='food_intakes',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='plans',
                to='food_app.foodintake',
                verbose_name='Приемы пищи',
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plan',
            name='persons',
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, '1 человек'),
                    (2, '2 человека'),
                    (3, '3 человека'),
                    (4, '4 человека'),
                    (5, '5 человек'),
                ],
                default=1,
                verbose_name='Кол-во человек',
            ),
        ),
    ]
