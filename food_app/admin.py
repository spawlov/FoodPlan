from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    AllergicCategory,
    FoodIntake,
    Menu,
    Plan,
    PlanPeriod,
    Product,
    Recipe,
    Ingredient,
    RecipeCategory,
    Subscription,
    Promocode,
)


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    list_filter = (
        'name',
        'description',
    )
    search_fields = (
        'name',
        'description',
    )


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    readonly_fields = ['price']
    list_display = (
        'price',
        'persons',
    )
    list_filter = (
        'price',
        'persons',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = (
        'title',
        'category',
        'cooking_time',
        'food_intake',
        'price',
        'get_photo'
    )
    list_filter = (
        'category',
        'food_intake',
        'price',
    )
    search_fields = (
        'title',
        'description',
        'cooking_method'
    )
    readonly_fields = (
        'get_photo',
    )

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        return 'No image attached'

    get_photo.short_description = "Картинка"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'calories_per_100g',
        'allergic_category',
    )
    list_filter = (
        'name',
        'calories_per_100g',
        'allergic_category',
    )
    search_fields = (
        'name',
        'calories_per_100g',
        'allergic_category',
    )


@admin.register(PlanPeriod)
class PlanPeriodAdmin(admin.ModelAdmin):
    list_display = ['duration']
    list_filter = ['duration']


@admin.register(FoodIntake)
class FoodIntake(admin.ModelAdmin):
    list_display = ['name']


@admin.register(AllergicCategory)
class AllergicCategory(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'is_active']


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = [
        'promocode',
        'start_at',
        'end_at',
        'discount'
    ]
    list_filter = [
        'promocode',
        'start_at',
        'end_at',
        'discount'
    ]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['date', 'recipe']
