from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """レシピカテゴリ"""
    name = models.CharField('カテゴリ名', max_length=100, unique=True)
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """レシピ"""
    DIFFICULTY_CHOICES = [
        (1, '簡単'),
        (2, '普通'),
        (3, '難しい'),
    ]

    title = models.CharField('タイトル', max_length=200)
    description = models.TextField('説明', blank=True)
    youtube_url = models.URLField('YouTube URL', blank=True, null=True)
    image = models.ImageField('画像', upload_to='recipes/', blank=True, null=True)
    
    # 調理情報
    cooking_time = models.PositiveIntegerField('調理時間（分）', default=30)
    servings = models.PositiveIntegerField('人数', default=2)
    difficulty = models.IntegerField(
        '難易度', 
        choices=DIFFICULTY_CHOICES, 
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    
    # 分類
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='カテゴリ'
    )
    
    # ユーザー情報
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='作成者'
    )
    
    # お気に入り
    favorites = models.ManyToManyField(
        User,
        through='RecipeFavorite',
        related_name='favorite_recipes',
        blank=True
    )
    
    # メタデータ
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    is_public = models.BooleanField('公開', default=True)

    class Meta:
        verbose_name = 'レシピ'
        verbose_name_plural = 'レシピ'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def favorite_count(self):
        """お気に入り数を取得"""
        return self.favorites.count()


class Ingredient(models.Model):
    """材料"""
    UNIT_CHOICES = [
        ('g', 'グラム'),
        ('kg', 'キログラム'),
        ('ml', 'ミリリットル'),
        ('l', 'リットル'),
        ('個', '個'),
        ('本', '本'),
        ('枚', '枚'),
        ('パック', 'パック'),
        ('袋', '袋'),
        ('缶', '缶'),
        ('大さじ', '大さじ'),
        ('小さじ', '小さじ'),
        ('カップ', 'カップ'),
        ('少々', '少々'),
        ('適量', '適量'),
    ]

    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='ingredients',
        verbose_name='レシピ'
    )
    name = models.CharField('材料名', max_length=100)
    amount = models.CharField('分量', max_length=50, blank=True)
    unit = models.CharField('単位', max_length=10, choices=UNIT_CHOICES, blank=True)
    notes = models.CharField('備考', max_length=200, blank=True)
    order = models.PositiveIntegerField('順序', default=0)

    class Meta:
        verbose_name = '材料'
        verbose_name_plural = '材料'
        ordering = ['order', 'id']

    def __str__(self):
        unit_display = f"{self.amount}{self.unit}" if self.amount and self.unit else self.amount or ""
        return f"{self.name} {unit_display}".strip()


class Step(models.Model):
    """手順"""
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='steps',
        verbose_name='レシピ'
    )
    step_number = models.PositiveIntegerField('手順番号')
    description = models.TextField('手順内容')
    image = models.ImageField('手順画像', upload_to='steps/', blank=True, null=True)
    cooking_time = models.PositiveIntegerField('所要時間（分）', blank=True, null=True)

    class Meta:
        verbose_name = '手順'
        verbose_name_plural = '手順'
        ordering = ['step_number']
        unique_together = ['recipe', 'step_number']

    def __str__(self):
        return f"{self.recipe.title} - 手順{self.step_number}"


class RecipeFavorite(models.Model):
    """レシピお気に入り"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='レシピ')
    created_at = models.DateTimeField('お気に入り登録日時', auto_now_add=True)

    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り'
        unique_together = ['user', 'recipe']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"


class RecipeRating(models.Model):
    """レシピ評価"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='レシピ')
    rating = models.IntegerField(
        '評価',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('コメント', blank=True)
    created_at = models.DateTimeField('評価日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '評価'
        verbose_name_plural = '評価'
        unique_together = ['user', 'recipe']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} ({self.rating}★)"
