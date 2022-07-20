from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet


app_name = "api"
router = routers.DefaultRouter()
router.register("recipes", RecipeViewSet)
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
