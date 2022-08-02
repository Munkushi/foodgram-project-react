from api.pagination import CustomPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from foodgram.models import (
    IngredientAmount, Ingredients, Recipe, ShoppingCart, Subscribe, Tag, Favorite
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filter import AuthorAndTagFilter, IngredientsFilter
from .permissions import AdminOrReadOnly, AuthorOrReadOnly
from .serializers import (
    IngredientsSerializer, RecipeGetSeriazlier, RecipePostSerializer,
    SubscribeSerializer, TagSerializer,
)
from .utils import download_shooping_card

User = get_user_model()


class UserViewset(UserViewSet):
    """Viewset для кастомной модели User."""

    pagination_class = CustomPagination

    @action(detail=True, permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        """Создание подписки."""

        user = request.user
        author = get_object_or_404(User, id=id)

        if (
            user == author
            or Subscribe.objects.filter(user=user, author=author).exists()
        ):
            return Response(
                {"errors": "Вы не можете это сделать."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow = Subscribe.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(follow, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        """Отписаться."""
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {"errors": "Вы не можете отписываться от самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow = Subscribe.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Вы уже отписались"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Получение данных о подписках."""

        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={"request": request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели Tag.
    Могут создавать только админы.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели Ingredients.
    Могут создавать только админы.
    """

    queryset = Ingredients.objects.all()
    permission_classes = (AdminOrReadOnly,)
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientsFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для модеил Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipePostSerializer
    pagination_class = CustomPagination
    filter_class = AuthorAndTagFilter
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Создание рецепта."""
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=("delete", "post"),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        """Добавить/убрать обьект в избранное или из него."""
        if request.method == "POST":
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(
        detail=True,
        methods=("delete", "post"),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление рецепта в/из корзину/ы"""
        if request.method == "POST":
            return self.add_obj(ShoppingCart, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {"errors": "Рецепт уже добавлен в список"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeGetSeriazlier(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Рецепт уже удален"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=("get",),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            "ingredient__name", "ingredient__measurement_unit",
            "amount")
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    "measurement_unit": item[1],
                    "amount": item[2]
                }
            else:
                final_list[name]["amount"] += item[2]

        download_shooping_card(final_list)
