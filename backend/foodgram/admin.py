from django.contrib import admin

from .models import Recipe, Ingredients, Tag, Subscribe, LikeIngredients, ShoppingCart


class RecipeAdmin(admin.ModelAdmin):
    """Админка для модели Рецепта."""
    
    empty_value_display = "-пусто-"
    list_display = (
        "author",
        "name",
        "text",
        "ingredients",
        "tag",
        "cooking_time"
    )

    search_fields = ("name", "author", "tag")

    list_filter = ("tag",)


class IngredientsAdmin(admin.ModelAdmin):
    """Админка для модели Ингредиента."""
    
    empty_value_display = "-пусто-"
    list_display = (
        "name",
        "measurement",
        "quantity"
    )

    search_fields = ("name",)


class TagAdmin(admin.ModelAdmin):
    """Админка для модели Тега."""
    
    empty_value_display = "-пусто-"
    list_display = (
        "name",
        "slug",
        "color"
    )

    filter_fields = ("name",)


admin.register(Recipe, RecipeAdmin)
admin.register(Ingredients, IngredientsAdmin)
admin.register(Tag, TagAdmin)
admin.register(Subscribe)
admin.register(LikeIngredients)
admin.register(ShoppingCart)