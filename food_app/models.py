from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=10, db_index=True, verbose_name="План")
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Картинка', blank=True)
    cooking_method = models.TextField(verbose_name="Способ приготовления")
    cooking_time = models.TimeField(db_index=True, verbose_name="Время готовки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update date')
    intake = models.CharField(max_length=10, verbose_name="Кол-во приемов пищи")
    ingredient = models.ManyToManyField('Ingredient', verbose_name="Ингредиенты")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['title']


class Ingredient(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name="Название")
    weight = models.FloatField(verbose_name="Вес")
    calories = models.FloatField(verbose_name="Калории")
    calories_per_100g = models.SmallIntegerField(db_index=True, verbose_name="Калории на 100 г.")
    allergy = models.ForeignKey('Allergy',
                                on_delete=models.PROTECT,
                                db_index=True,
                                verbose_name="Аллергии")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиент'
        ordering = ['title']


class Allergy(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    ingredient = models.ForeignKey(Ingredient,
                                   db_index=True,
                                   on_delete=models.CASCADE,
                                   verbose_name="Продукт")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'
        ordering = ['title']


class RecipeCategory(models.Model):
    title = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['title']


class Plan(models.Model):
    period = models.IntegerField(db_index=True, verbose_name="Срок подписки")
    MEAL_CHOICES = (
        ('breakfast', 'breakfast'),
        ('dinner', 'dinner'),
        ('supper', 'supper'),
        ('dessert', 'dessert'),
    )
    meal = models.CharField(max_length=1, choices=MEAL_CHOICES)
    price = models.SmallIntegerField(verbose_name="Цена")
    persons = models.SmallIntegerField(verbose_name="Кол-во человек")
    allergy = models.ForeignKey(Allergy, on_delete=models.PROTECT)

    def __str__(self):
        return self.period

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ['period']


class Subscription(models.Model):
    start = models.DateField(auto_now_add=True, verbose_name='Начало подписки', db_index=True)
    end = models.DateField(verbose_name='Конец подписки', db_index=True)
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Статус')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name='План')

    def __str__(self):
        return f'С {self.start} до {self.end}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['is_active']


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subscription = models.OneToOneField(Subscription,
                                        on_delete=models.PROTECT,
                                        verbose_name='Чек',
                                        related_name='subscription')

