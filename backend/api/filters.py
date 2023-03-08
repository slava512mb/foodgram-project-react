from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import django_filters as filters

from recipes.models import Ingredient, Recipe

User, Subscribe = get_user_model()

class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagsMultipleChoiceField(
        filters.fields.MultipleChoiceField):
    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'],
                code='required')
        for val in value:
            if val in self.choices and not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},)


class TagsFilter(filters.AllValuesMultipleFilter):
    field_class = TagsMultipleChoiceField


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='Корзина')
    is_favorited = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='Избранное')
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Ссылки')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']
