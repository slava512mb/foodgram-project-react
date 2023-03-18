from django.contrib import admin
from django.contrib.admin import register, display

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

EMPTY_MESSAGE = '-пусто-'


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_author',
        'name',
        'text',
        'cooking_time',
        'get_tags',
        'get_ingredients',
        'pub_date',
        'get_favorite_count',
    )
    search_fields = (
        'name',
        'cooking_time',
        'author__email',
        'ingredients__name',
    )
    list_filter = (
        'pub_date',
        'tags',
    )
    inlines = (RecipeIngredientAdmin,)
    empty_value_display = EMPTY_MESSAGE

    @display(
        description='Электронная почта автора')
    def get_author(self, obj):
        return obj.author.email

    @display(description='Тэги')
    def get_tags(self, obj):
        list_ = [_.name for _ in obj.tags.all()]
        return ', '.join(list_)

    @display(description=' Ингредиенты ')
    def get_ingredients(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])

    @display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite_recipe.count()


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )
    empty_value_display = EMPTY_MESSAGE


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    empty_value_display = EMPTY_MESSAGE


@register(ShoppingCart)
class SoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_recipe',
        'get_count'
    )
    empty_value_display = EMPTY_MESSAGE

    @display(description='Рецепты')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @display(description='В избранных')
    def get_count(self, obj):
        return obj.recipe.count()


@register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_recipe',
        'get_count',
    )
    empty_value_display = EMPTY_MESSAGE

    @display(
        description='Рецепты')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @display(
        description='В избранных')
    def get_count(self, obj):
        return obj.recipe.count()
