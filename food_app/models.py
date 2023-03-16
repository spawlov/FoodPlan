from tabnanny import verbose
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RecipeCategory(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Картинка', blank=True)
    cooking_method = models.TextField('Способ приготовления')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    category = models.ForeignKey(
        RecipeCategory,
        verbose_name='Меню',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    calories = models.PositiveSmallIntegerField(
        'Калории(Ккал)',
        default=0,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки (мин)',
        default=1,
        blank=True,
        null=True,
    )
    food_intake = models.ForeignKey(
        'FoodIntake',
        verbose_name='Прием пищи',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ingredient = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['cooking_time']),
        ]

    def __str__(self):
        return self.title


class AllergicCategory(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория аллергенных продуктов'
        verbose_name_plural = 'Категории аллергенных продуктов'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=150)
    weight = models.FloatField('Вес(граммы)')
    calories_per_100g = models.PositiveSmallIntegerField('Калории на 100 г.')
    allergic_category = models.ForeignKey(
        AllergicCategory,
        verbose_name='Категории аллергенов',
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['calories_per_100g']),
        ]

    def __str__(self):
        return self.name


class FoodIntake(models.Model):
    name = models.CharField('Прием пищи', max_length=30)

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class PlanPeriod(models.Model):
    duration = models.PositiveSmallIntegerField('Срок подписки', default=1)

    class Meta:
        verbose_name = 'Срок подписки'
        verbose_name = 'Сроки подписок'
        indexes = [models.Index(fields=['duration'])]

    def __str__(self):
        if self.duration % 10 == 1 and self.duration % 100 != 11:
            month = 'месяц'
        elif 2 <= self.duration % 10 <= 4 and (
            self.duration % 100 < 10 or self.duration % 100 >= 20
        ):
            month = 'месяца'
        else:
            month = 'месяцев'

        return f'Подписка на {self.duration} {month}'


class Plan(models.Model):
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    persons = models.PositiveSmallIntegerField('Кол-во человек', default=1)
    period = models.OneToOneField(
        PlanPeriod, verbose_name="Срок подписки", related_name='plan', on_delete=models.CASCADE
    )
    allergies = models.ForeignKey(
        AllergicCategory,
        verbose_name='Аллергии',
        related_name='plans',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        indexes = [
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f'План #{self.id}'


class Subscription(models.Model):
    start = models.DateField('Начало подписки', auto_now_add=True)
    end = models.DateField('Окончание подписки')
    is_active = models.BooleanField('Статус', default=False)
    plan = models.OneToOneField(Plan, verbose_name='План', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        indexes = [
            models.Index(fields=['start']),
            models.Index(fields=['end']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f'С {self.start} до {self.end}'
