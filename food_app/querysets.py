from django.db import models


class RecipeQuerySet(models.QuerySet):
    def with_calories(self):
        calories_per_100 = 'ingredients__product__calories_per_100g'

        return self.annotate(
            total_calories=models.Sum(
                models.F('ingredients__quantity') / 100 * models.F(calories_per_100)
            ),
        )
