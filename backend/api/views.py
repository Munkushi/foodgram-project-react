from django import views
from foodgram.models import Tag, Recipe, Ingredients, ShoppingCart, LikeIngredients, Subscribe, IngredientAmount
# from core.permissions import AuthorAdminOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import RecipeGetSeriazlier, RecipePostSerializer


User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Tag."""

    # serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None



class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для моедил Recipe."""

    pass

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSeriazlier
        return RecipePostSerializer