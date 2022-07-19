# Generated by Django 2.2.16 on 2022-07-13 10:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=200, verbose_name='Название')),
                ('measurement_unit', models.TextField(blank=True, verbose_name='Единица измерения')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=200, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Представление тега')),
                ('color', models.CharField(choices=[('#ff0006', 'Красный'), ('#879eee', 'Голубой'), ('#220e75', 'Синий'), ('#e784f4', 'Розовый'), ('#8fd8b9', 'Светло зелёный'), ('#faad62', 'Светло оранжевый'), ('#deec59', 'Жёлтый'), ('#7e4bf3', 'Фиолетовый')], default='#ffffff', max_length=7, unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=200, verbose_name='Название')),
                ('image', models.ImageField(blank=True, upload_to='backend/', verbose_name='Картинка')),
                ('text', models.CharField(blank=True, max_length=300, verbose_name='Текствое описание')),
                ('cooking_time', models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1, message='Минимальное время должно быть 1 минута!')], verbose_name='Время приготовления (м.)')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('cart', models.ManyToManyField(related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Список покупок')),
                ('favorite', models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Понравившиеся рецепты')),
                ('ingredients', models.ManyToManyField(blank=True, related_name='recipes', to='foodgram.Ingredients', verbose_name='Ингредиент')),
                ('tag', models.ManyToManyField(blank=True, to='foodgram.Tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='LikeIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_ingredient', to='foodgram.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_ingredient', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество ингредиентов')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.Ingredients', verbose_name='Ингридиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.Recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Количество ингридиента',
                'verbose_name_plural': 'Количество ингридиентов',
                'ordering': ['-id'],
            },
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_following'),
        ),
        migrations.AddConstraint(
            model_name='likeingredients',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='У вас уже добавлен такой рецепт.'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique ingredients recipe'),
        ),
    ]
