import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import related
from django_ckeditor_5.fields import CKEditor5Field


class RecipeCategory(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', null=True, blank=True)
    image = models.ImageField('Картинка', upload_to='photos/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField('Название', max_length=150)
    description = CKEditor5Field('Описание', config_name='extends')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Картинка', blank=True)
    cooking_method = CKEditor5Field('Способ приготовления', config_name='extends')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    price = models.DecimalField(
        'Стоимость блюда',
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    calories = models.PositiveSmallIntegerField('Калории', null=True, blank=True)
    category = models.ForeignKey(
        RecipeCategory,
        verbose_name='Меню',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    allergic_categories = models.ManyToManyField(
        'AllergicCategory',
        verbose_name='Категории аллергенов',
        related_name='recipes',
        blank=True,
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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['cooking_time']),
            models.Index(fields=['calories']),
            models.Index(fields=['price']),
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


class Product(models.Model):
    name = models.CharField('Название', max_length=150)
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
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['calories_per_100g']),
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    class UnitChoice(models.TextChoices):
        GRAMM = 'gram', 'гр.'
        ITEM = 'item', 'шт.'
        SLICE = 'slice', 'дол.'
        SPOON_SMALL = 'spoon_small', 'ч.л.'
        SPOON = 'spoon', 'ст.л.'
        VOLUME = 'volume', 'мл.'
        PITCH = 'pitch', 'щеп.'

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='ingredients',
        on_delete=models.CASCADE,
    )
    unit = models.CharField(
        'Единицы',
        max_length=20,
        choices=UnitChoice.choices,
    )
    quantity = models.FloatField('Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.quantity} г'


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
    price = models.DecimalField(
        'Стоимость периода',
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Срок подписки'
        verbose_name_plural = 'Сроки подписок'
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

        return f'{self.duration} {month}'


class Plan(models.Model):
    class PersonChoice(models.IntegerChoices):
        ONE = 1, '1 человек'
        TWO = 2, '2 человека'
        THREE = 3, '3 человека'
        FOUR = 4, '4 человека'
        FIVE = 5, '5 человек'

    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    persons = models.PositiveSmallIntegerField(
        'Кол-во человек',
        choices=PersonChoice.choices,
        default=PersonChoice.ONE,
    )
    period = models.ForeignKey(
        PlanPeriod, verbose_name="Срок подписки", related_name='plan', on_delete=models.PROTECT
    )
    recipe_category = models.ForeignKey(
        RecipeCategory,
        verbose_name='Меню',
        related_name='plans',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    allergies = models.ManyToManyField(
        AllergicCategory,
        verbose_name='Аллергии',
        related_name='plans',
        blank=True,
    )
    food_intakes = models.ManyToManyField(
        FoodIntake,
        verbose_name='Приемы пищи',
        related_name='plans',
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
    start = models.DateTimeField('Начало подписки', auto_now_add=True)
    end = models.DateTimeField('Окончание подписки')
    is_active = models.BooleanField('Статус', default=False)
    paid = models.BooleanField('Статус оплаты', default=False)
    plan = models.OneToOneField(
        Plan,
        verbose_name='План',
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        on_delete=models.SET_NULL,
        related_name='subscriptions',
        null=True,
        blank=True,
    )
    promocode = models.ForeignKey(
        'Promocode',
        verbose_name='Промокод',
        on_delete=models.SET_NULL,
        related_name='subscriptions',
        null=True,
        blank=True,
    )

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


def get_uploading_path(instance, filename):
    return os.path.join(str(instance.user.username), filename)


class Customer(models.Model):
    user = models.OneToOneField(
        User, related_name='customer', on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    avatar = models.ImageField(upload_to=get_uploading_path, blank=True, verbose_name='Аватар')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user.username


class Promocode(models.Model):
    promocode = models.CharField(max_length=10)
    start_at = models.DateField("Начало действия промокода")
    end_at = models.DateField("Конец действия промокода")
    discount = models.SmallIntegerField("Размер скидки")

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        indexes = [
            models.Index(fields=['start_at']),
            models.Index(fields=['end_at']),
            models.Index(fields=['discount']),
        ]

    def __str__(self):
        return self.promocode


class Menu(models.Model):
    date = models.DateField('Дата')
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='menu_items',
        on_delete=models.CASCADE,
    )
    subscription = models.ForeignKey(
        Subscription,
        verbose_name='Подписка',
        related_name='menus',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return f'{self.recipe.title} на f{self.date}'
