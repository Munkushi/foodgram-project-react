from foodgram.models import Tag, Recipe, Ingredients, Subscribe, IngredientAmount, ShoppingCart
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from djoser.views import UserViewSet
from api.pagination import CustomPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import RecipeGetSeriazlier, RecipePostSerializer, TagSerializer, IngredientsSerializer, UserSubscribeSerializer, SubscribeSerializer
from .permissions import AdminOrReadOnly, AuthorOrReadOnly
from .filter import IngredientsFilter, AuthorAndTagFilter
from rest_framework.response import Response



User = get_user_model()



class UserViewset(UserViewSet):
    """Viewset для кастомной модели User."""

    pagination_class = CustomPagination

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Создание подписки."""

        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                "errors": "Вы не можете подписываться на самого себя"
            }, status=status.HTTP_400_BAD_REQUEST)
        if Subscribe.objects.filter(user=user, author=author).exists():
            return Response({
                "errors": "Вы уже подписаны на данного пользователя"
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Subscribe.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        """Отписаться."""
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                "errors": "Вы не можете отписываться от самого себя"
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Subscribe.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            "errors": "Вы уже отписались"
        }, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Tag."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None



class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    permission_classes = (AdminOrReadOnly,)
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientsFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для моедил Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipePostSerializer
    pagination_class = CustomPagination 
    filter_class = AuthorAndTagFilter
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Создание рецепта."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=["get", "delete"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Добавить/убрать обьект в избранное или из него."""
        if request.method == "GET":
            return self.add_obj(Subscribe, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(Subscribe, request.user, pk)
        return None

    @action(detail=True, methods=["get", "delete"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление рецепта в/из корзину/ы"""
        if request.method == "GET":
            return self.add_obj(ShoppingCart, request.user, pk)
        elif request.method == "DELETE":
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                "errors": "Рецепт уже добавлен в список"
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeGetSeriazlier(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            "errors": "Рецепт уже удален"
        }, status=status.HTTP_400_BAD_REQUEST)