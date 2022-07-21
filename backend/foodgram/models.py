from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


# colors for Tag
RED = "#ff0006"
LIGHT_BLUE = "#879eee"
BLUE = "#220e75"
PINK = "#e784f4"
LIGHT_GREEN = "#8fd8b9"
LIGHT_ORANGE = "#faad62"
YELLOW = "#deec59"
PURPLE = "#7e4bf3"


COLORS = [
    (RED, "Красный"),
    (LIGHT_BLUE, "Голубой"),
    (BLUE, "Синий"),
    (PINK, "Розовый"),
    (LIGHT_GREEN, "Светло зелёный"),
    (LIGHT_ORANGE, "Светло оранжевый"),
    (YELLOW, "Жёлтый"),
    (PURPLE, "Фиолетовый"),
]


class Tag(models.Model):
    """Тег у рецепта."""

    name = models.TextField(
        "Название", unique=True, blank=True, max_length=200)
    slug = models.SlugField(
        verbose_name="Представление тега", unique=True, max_length=200)
    color = models.CharField(
        verbose_name="Цвет",
        max_length=7, 
        choices=COLORS, 
        default="#ffffff", 
        unique=True
    )


    class Meta:
        ordering = ("-id",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ингредиенты."""

    name = models.TextField(
        verbose_name="Название", 
        max_length=200, 
        unique=True
        )
    measurement_unit = models.TextField(
        verbose_name="Единица измерения", 
        unique=True
        )

    class Meta:
        ordering = ("-id",)
    
    
    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Основная модель, рецепт."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    name = models.TextField(
        max_length=200, 
        verbose_name="Название")
    image = models.ImageField(
        upload_to="backend/", 
        verbose_name="Картинка")
    text = models.CharField(
        verbose_name="Текствое описание", 
        max_length=300)
    ingredients = models.ManyToManyField(
        Ingredients, 
        related_name="recipes", 
        verbose_name="Ингредиент", 
    )
    tag = models.ManyToManyField(
        Tag, 
        verbose_name="Тег")
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (м.)",
        validators=(
            validators.MinValueValidator(1, message="Минимальное время - 1 минута!"),
        ),
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.description[:20]


class IngredientAmount(models.Model):
    """
    Количество нужных ингредиентов.
    """

    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиентов")

    class Meta:
        ordering = ["-id"]
        verbose_name = "Количество ингридиента"
        verbose_name_plural = "Количество ингридиентов"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"], 
                name="unique ingredients recipe"
            )
        ]


class Subscribe(models.Model):
    """Подписаться на автора."""

    user = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_following")
        ]

        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f"{self.user}: {self.author}."


class ShoppingCart(models.Model):
    """Модель для корзины."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Корзина"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique cart user")
        ]


class Favorite(models.Model):
    """Модель для добавления рецепта в избранное."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
