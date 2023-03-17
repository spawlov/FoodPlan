from django import forms

from food_app.models import FoodIntake, Plan, AllergicCategory, PlanPeriod, RecipeCategory


class OrderForm(forms.Form):
    recipe_categories = forms.ModelChoiceField(
        queryset=RecipeCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    food_intakes = forms.ModelMultipleChoiceField(
        queryset=FoodIntake.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input me-1 foodplan_checked-green'})
    )
    allergies = forms.ModelMultipleChoiceField(
        queryset=AllergicCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input me-1 foodplan_checked-green'})
    )
    period = forms.ModelChoiceField(
        queryset=PlanPeriod.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    persons = forms.ChoiceField(
        choices=[(count, count) for count in range(1, 7)],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
