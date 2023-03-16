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


class PaymentForm(forms.Form):
    card_name = forms.CharField(min_length=2, label='Имя владельца')
    card_number = forms.CharField(min_length=16, max_length=16, label='Номер карты')
    card_month = forms.IntegerField(min_value=1, max_value=12, label='Месяц')
    card_day = forms.IntegerField(min_value=1, max_value=31, label='День')
    card_cvc = forms.CharField(min_length=3, max_length=3, label='CVC')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Field attrs
        self.fields['card_name'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Имя Фамилия',
                'type': 'text',
                'id': 'card-name',
                'pattern': '[a-zA-Z ]+',
            }
        )
        self.fields['card_number'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': '1234 5678 9123 4561',
                'type': 'number',
                'id': 'card-number',
                'oninput': 'this.value = this.value.slice(0, 16)',
                'min': '0',
            }
        )
        self.fields['card_month'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'MM',
                'type': 'number',
                'id': 'expiry-date-month',
                'pattern': '(0[1-9]|1[0-2])\/[0-9]{2}',
                'oninput': 'this.value = this.value.slice(0, 2)',
            }
        )
        self.fields['card_day'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'ДД',
                'type': 'number',
                'id': 'expiry-date-day',
                'pattern': '(0[1-9]|1[0-2])\/[0-9]{2}',
                'oninput': 'this.value = this.value.slice(0, 2)',
            }
        )
        self.fields['card_cvc'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': '123',
                'type': 'number',
                'id': 'cvc',
                'oninput': 'this.value = this.value.slice(0, 3)',
            }
        )

        # Label attrs
        self.fields['card_name'].label_attrs = {'class': 'form-label'}
        self.fields['card_number'].label_attrs = {'class': 'form-label'}
        self.fields['card_month'].label_attrs = {'class': 'form-label'}
        self.fields['card_day'].label_attrs = {'class': 'form-label'}
        self.fields['card_cvc'].label_attrs = {'class': 'form-label'}
