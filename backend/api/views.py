from api.pagination import CustomPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
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
from foodgram.models import (
    Favorite, IngredientAmount, Ingredients, Recipe, ShoppingCart, Subscribe,
    Tag,
)

User = get_user_model()


class UserViewset(UserViewSet):
    """Viewset для кастомной модели User."""

    pagination_class = CustomPagination

    @action(
        detail=True,
        permission_classes=(IsAuthenticated,),
        methods=("post", "delete",),
    )
    def subscribe(self, request, id=None):
        """Подписка/Отписка."""
        author = get_object_or_404(User, id=id)
        if request.method == "POST" or request.method == "DELETE":
            if request.user == author:
                raise Response({
                    "errors": "Нельзя подписываться на себя."},
                    status=status.HTTP_400_BAD_REQUEST)
        if request.method == "POST":
            if Subscribe.objects.filter(user=request.user, 
            author=author).exists():
                return Response({
                    "errors": "Вы уже подписаны на данного пользователя"
                }, status=status.HTTP_400_BAD_REQUEST)

            follow = Subscribe.objects.create(user=request.user, author=author)
            serializer = SubscribeSerializer(
                follow, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            follow = Subscribe.objects.filter(user=request.user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({
                "errors": "Вы уже отписались"
            }, status=status.HTTP_400_BAD_REQUEST)

        return None        

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Список подписок пользователя."""
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={"request": request}
        )
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
            "ingredient__name",
            "ingredient__measurement_unit",
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

        return download_shooping_card(final_list)
