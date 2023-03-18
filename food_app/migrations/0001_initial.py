# Generated by Django 3.2.16 on 2023-03-16 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllergicCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория аллергенных продуктов',
                'verbose_name_plural': 'Категории аллергенных продуктов',
            },
        ),
        migrations.CreateModel(
            name='FoodIntake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Прием пищи')),
            ],
            options={
                'verbose_name': 'Прием пищи',
                'verbose_name_plural': 'Приемы пищи',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('weight', models.FloatField(verbose_name='Вес(граммы)')),
                ('calories_per_100g', models.PositiveSmallIntegerField(verbose_name='Калории на 100 г.')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('persons', models.PositiveSmallIntegerField(default=1, verbose_name='Кол-во человек')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.CreateModel(
            name='PlanPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveSmallIntegerField(default=1, verbose_name='Срок подписки')),
            ],
            options={
                'verbose_name': 'Сроки подписок',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Картинка')),
                ('cooking_method', models.TextField(verbose_name='Способ приготовления')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('calories', models.PositiveSmallIntegerField(default=0, verbose_name='Калории(Ккал)')),
                ('cooking_time', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Время готовки (мин)')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(auto_now_add=True, verbose_name='Начало подписки')),
                ('end', models.DateField(verbose_name='Окончание подписки')),
                ('is_active', models.BooleanField(default=False, verbose_name='Статус')),
                ('plan', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='food_app.plan', verbose_name='План')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddIndex(
            model_name='recipecategory',
            index=models.Index(fields=['name'], name='food_app_re_name_e01128_idx'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='food_app.recipecategory', verbose_name='Меню'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='food_intake',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='food_app.foodintake', verbose_name='Прием пищи'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='recipes', to='food_app.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddIndex(
            model_name='planperiod',
            index=models.Index(fields=['duration'], name='food_app_pl_duratio_a88078_idx'),
        ),
        migrations.AddField(
            model_name='plan',
            name='allergies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plans', to='food_app.allergiccategory', verbose_name='Аллергии'),
        ),
        migrations.AddField(
            model_name='plan',
            name='period',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='food_app.planperiod', verbose_name='Срок подписки'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='allergic_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='food_app.allergiccategory', verbose_name='Категории аллергенов'),
        ),
        migrations.AddIndex(
            model_name='foodintake',
            index=models.Index(fields=['name'], name='food_app_fo_name_31b056_idx'),
        ),
        migrations.AddIndex(
            model_name='allergiccategory',
            index=models.Index(fields=['name'], name='food_app_al_name_895e36_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['start'], name='food_app_su_start_e32d69_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['end'], name='food_app_su_end_4201e5_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['is_active'], name='food_app_su_is_acti_1e95ed_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['title'], name='food_app_re_title_bdd156_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['cooking_time'], name='food_app_re_cooking_fe9df8_idx'),
        ),
        migrations.AddIndex(
            model_name='plan',
            index=models.Index(fields=['price'], name='food_app_pl_price_77dc33_idx'),
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='food_app_in_name_7ae73a_idx'),
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['calories_per_100g'], name='food_app_in_calorie_4a79ba_idx'),
        ),
    ]