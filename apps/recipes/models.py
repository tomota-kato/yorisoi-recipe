from django.db import models
from django.contrib.auth.models import User
from apps.ingredients.models import Ingredient


class Recipe(models.Model):
    """レシピ"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="作成者"
    )
    name = models.CharField(
        max_length=200, 
        verbose_name="レシピ名"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="説明"
    )
    instructions = models.TextField(
        verbose_name="作り方",
        help_text="調理手順を記述してください"
    )
    cooking_time = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name="調理時間（分）"
    )
    servings = models.PositiveIntegerField(
        default=2, 
        verbose_name="人数分"
    )
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', '簡単'),
            ('medium', '普通'),
            ('hard', '難しい'),
        ],
        default='medium',
        verbose_name="難易度"
    )
    
    # AIアシスト関連
    source_url = models.URLField(
        blank=True, 
        verbose_name="参照URL",
        help_text="YouTubeなどの参照元URL"
    )
    is_ai_generated = models.BooleanField(
        default=False, 
        verbose_name="AI生成",
        help_text="AIによって生成されたレシピかどうか"
    )
    ai_analysis_data = models.JSONField(
        null=True, 
        blank=True, 
        verbose_name="AI解析データ",
        help_text="AIによる解析結果のJSONデータ"
    )
    
    # 画像
    image = models.ImageField(
        upload_to='recipes/images/', 
        blank=True, 
        null=True, 
        verbose_name="画像"
    )
    
    # タグ機能
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="タグ",
        help_text="カンマ区切りでタグを入力（例: 和食,簡単,30分以内）"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "レシピ"
        verbose_name_plural = "レシピ"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        """タグをリスト形式で取得"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class RecipeIngredient(models.Model):
    """レシピの材料"""
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='recipe_ingredients',
        verbose_name="レシピ"
    )
    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE, 
        verbose_name="材料"
    )
    quantity = models.CharField(
        max_length=50, 
        verbose_name="分量",
        help_text="例: 1個、200g、大さじ2"
    )
    is_optional = models.BooleanField(
        default=False, 
        verbose_name="オプション",
        help_text="必須でない材料の場合はチェック"
    )
    order = models.PositiveIntegerField(
        default=1, 
        verbose_name="表示順序"
    )

    class Meta:
        verbose_name = "レシピ材料"
        verbose_name_plural = "レシピ材料"
        ordering = ['order', 'id']
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}: {self.quantity}"


class RecipeFavorite(models.Model):
    """レシピお気に入り"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="ユーザー"
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        verbose_name="レシピ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="お気に入り登録日時")

    class Meta:
        verbose_name = "お気に入りレシピ"
        verbose_name_plural = "お気に入りレシピ"
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}" 