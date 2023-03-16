from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import duration


class RecipeCategory(models.Model):
    name = models.CharField('Название')
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
        validator=[MinValueValidator(0)],
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки (мин)',
        default=1,
        blank=True,
        null=True,
        validator=[MinValueValidator(1)],
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
    calories = models.PositiveSmallIntegerField(
        'Калории(Ккал)',
        default=0,
        validators=[MinValueValidator(0)],
    )
    calories_per_100g = models.PositiveSmallIntegerField(
        'Калории на 100 г.',
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
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
            models.Index(fields=['cooking_time']),
        ]

    def __str__(self):
        return self.name


class FoodIntake(models.Model):
    name = models.CharField('Прием пищи', max_length=30)
    plan =

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self) -> str:
        return self.name


class PlanPeriod(models.Model):
    duration = models.PositiveBigIntegerField(
        'Срок подписки',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(24)],
    )
    price = models.PositiveSmallIntegerField('Цена', default=100)


    class Meta:
        verbose_name = 'Период подписки'
        verbose_name = 'Периоды подписок'
        indexes = [
            models.Index(fields=['duration']),
            models.Index(fields=['price']),
        ]

    def __str__(self) -> str:
        return f'Подписка на: {duration} месяцев'


class Plan(models.Model):
    # period = models.OneToOneField(PlanPeriod, verbose_name="Срок подписки")

    class Plan(models.IntegerChoices):
        ONE = 1, 1
        THREE = 3, 3
        TWELVE= 6, 6



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
