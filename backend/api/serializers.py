from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from foodgram.models import (
    IngredientAmount, Ingredients, Recipe, Subscribe, Tag,
)
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserCreateSerializer):
    """Сериализатор для создания User."""

    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        # Обязательные поля
        extra_kwargs = {
            "password": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "email": {"required": True},
            "last_name": {"required": True},
        }


class RecipeGetSeriazlier(serializers.ModelSerializer):
    """Serializer для модели Recipe. GET"""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("__all__",)


class UserSerializer(UserSerializer):
    """Подписки пользователя."""

    is_subscribed = serializers.SerializerMethodField(
        method_name="get_is_subscribed")

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        read_only_fields = ("__all__",)

    def get_is_subscribed(self, obj):
        """Получение данных о подписке."""
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    """Serializer для модели Tag."""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer для модели Igredients."""

    class Meta:
        model = Ingredients
        fields = "__all__"


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer для модели IgredientAmount."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientAmount
        fields = ("id",
                  "name",
                  "measurement_unit",
                  "amount")


class RecipePostSerializer(serializers.ModelSerializer):
    """Serializer для модели Recipe. POST"""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True, read_only=True, source="ingredientamount_set")
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = (
            "is_favorite",
            "is_shopping_cart",
        )

    def get_is_in_shopping_cart(self, obj):
        """Получение информации о нахождении рецепта."""
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def get_is_favorited(self, obj):
        """Получение списка изранного."""
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def create_ingredients(self, ingredients, recipe):
        """Получение ингредиентов для рецепта."""

        for ingredient in ingredients:
            IngredientAmount.objects.get_or_create(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )

    def create(self, validated_data):
        """Создание рецепта."""
        image = validated_data.pop("image")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get("tags")
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, recipe, validated_data):
        """Обновление данных о рецепте."""
        ingredients = validated_data.pop("ingredients")
        recipe.ingredients.clear()
        tags = validated_data.pop("tags")
        self.save_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def validate(self, data):
        """Валидация рецепта."""
        ingredients = self.initial_data.get("ingredients")
        if not ingredients:
            raise serializers.ValidationError(
                {
                    "ingredients": "Минимум один ингридиент"
                }
            )
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredients, id=ingredient_item["id"])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    "Ингридиенты должны " "быть уникальными"
                )
            ingredient_list.append(ingredient)
            if int(ingredient_item["amount"]) < 0:
                raise serializers.ValidationError(
                    {
                        "ingredients": (
                            "Убедитесь, что значение количества ингр. > 0."
                        )
                    }
                )
        data["ingredients"] = ingredients
        return data

    def validate_cooking_time(self, cooking_time):
        """Валидация времени приготовления."""
        if int(cooking_time) <= 1:
            raise serializers.ValidationError(
                "Минимальное время приготовления - 1 минута.")
        return cooking_time


class SubscribeSerializer(serializers.ModelSerializer):
    """Serializer для подписки."""
    id = serializers.ReadOnlyField(source="author.id")
    email = serializers.ReadOnlyField(source="author.email")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[: int(limit)]
        return RecipeGetSeriazlier(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
