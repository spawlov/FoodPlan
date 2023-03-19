from django.contrib import admin

from .models import (
    AllergicCategory,
    FoodIntake,
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
