from curses import panel
from django import forms

from food_app.models import Plan, PlanPeriod, RecipeCategory


class OrderForm(forms.ModelForm):
    error_css_class = 'text-danger fw-semibold'

    class Meta:
        model = Plan
        fields = ['persons', 'period', 'allergies', 'food_intakes', 'recipe_category']
        widgets = {
            'recipe_category': forms.Select(attrs={'class': 'form-select'}, ),
            'food_intakes': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input me-1 foodplan_checked-green'},
            ),
            'allergies': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input me-1 foodplan_checked-green'},
            ),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'persons': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        recipe_categories = RecipeCategory.objects.order_by('name')
        periods = PlanPeriod.objects.order_by('duration')

        self.fields['recipe_category'].initial = recipe_categories.first()
        self.fields['period'].initial = periods.first()

        self.fields['recipe_category'].empty_label = None
        self.fields['period'].empty_label = None
        self.fields['food_intakes'].empty_label = None

        self.fields['allergies'].required = True


class PaymentForm(forms.Form):
    card_name = forms.CharField(min_length=2, label='Имя владельца')
    card_number = forms.CharField(min_length=16, max_length=16, label='Номер карты')
    card_month = forms.IntegerField(min_value=1, max_value=12, label='Месяц')
    card_year = forms.IntegerField(min_value=23, max_value=50, label='Год')
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
        self.fields['card_year'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'ГГ',
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
        self.fields['card_year'].label_attrs = {'class': 'form-label'}
        self.fields['card_cvc'].label_attrs = {'class': 'form-label'}
