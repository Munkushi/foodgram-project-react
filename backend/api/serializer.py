from rest_framework import serializers

from foodgram.models import Tag, Recipe, Ingredients, IngredientAmount, LikeIngredients, Subscribe, ShoppingCart
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer для модели User."""
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )



# ONLY GET 
class TagSerializer(serializers.ModelSerializer):
    """Serializer для модели Tag."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")



# GET
class RecipeGetSeriazlier(serializers.ModelSerializer):
    """Serializer для модели Recipe. GET"""

    class Meta:
        model = Recipe
        fields = ("id", "tag", "author", "ingredients", "name", "image", "text", "cooking_time", "", "",)
        # is_favorited
        # is_in_shopping_cart


# POST
class RecipePostSerializer(serializers.ModelSerializer):
    """Serializer для модели Recipe. POST"""

    class Meta:
        model = Recipe
        fields = ("ingredients", "tag", "image", "name", "text", "cooking_time")




# GET. ПОЛУЧЕНИЕ ИНГРЕДИЕНТОВ
class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer для модели Igredients."""

    class Meta:
        model = Ingredients
        fields = ("id", "name", "measurement_unit",)
