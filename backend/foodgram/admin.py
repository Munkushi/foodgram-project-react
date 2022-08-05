from django.contrib.admin import ModelAdmin, TabularInline, register

from .models import IngredientAmount, Ingredients, Recipe, Subscribe, Tag


class IngredientInline(TabularInline):
    model = IngredientAmount
    extra = 2


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """Админка для модели Рецепта."""

    empty_value_display = "-пусто-"
    list_display = ("author", "name", "text", "cooking_time")

    search_fields = ("name", "author", "tags")

    list_filter = ("tags",)

    inlines = (IngredientInline)


@register(Ingredients)
class IngredientsAdmin(ModelAdmin):
    """Админка для модели Ингредиента."""

    empty_value_display = "-пусто-"
    list_display = ("name", "measurement_unit")

    search_fields = ("name",)


@register(Tag)
class TagAdmin(ModelAdmin):
    """Админка для модели Тега."""

    empty_value_display = "-пусто-"
    list_display = ("name", "slug", "color")

    filter_fields = ("name",)


register(Subscribe)
