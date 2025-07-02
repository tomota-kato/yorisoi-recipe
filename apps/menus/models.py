from django.db import models
from django.contrib.auth.models import User
from apps.recipes.models import Recipe
from datetime import datetime, timedelta


class WeeklyMenu(models.Model):
    """週単位の献立"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="ユーザー"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="献立名",
        help_text="例: 2024年1月第1週の献立"
    )
    start_date = models.DateField(
        verbose_name="開始日（月曜日）",
        help_text="その週の月曜日の日付"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="説明・メモ"
    )
    is_template = models.BooleanField(
        default=False, 
        verbose_name="テンプレート",
        help_text="再利用可能なテンプレートとして保存"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "週献立"
        verbose_name_plural = "週献立"
        ordering = ['-start_date']
        unique_together = ['user', 'start_date']

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    @property
    def end_date(self):
        """その週の日曜日の日付を取得"""
        return self.start_date + timedelta(days=6)

    @property
    def week_display(self):
        """週の表示用文字列"""
        return f"{self.start_date.strftime('%m/%d')} - {self.end_date.strftime('%m/%d')}"


class WeeklyMenuRecipe(models.Model):
    """週献立のレシピ割り当て"""
    MEAL_CHOICES = [
        ('breakfast', '朝食'),
        ('lunch', '昼食'),
        ('dinner', '夕食'),
    ]
    
    DAY_CHOICES = [
        (0, '月曜日'),
        (1, '火曜日'),
        (2, '水曜日'),
        (3, '木曜日'),
        (4, '金曜日'),
        (5, '土曜日'),
        (6, '日曜日'),
    ]

    weekly_menu = models.ForeignKey(
        WeeklyMenu, 
        on_delete=models.CASCADE, 
        related_name='menu_recipes',
        verbose_name="週献立"
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        verbose_name="レシピ"
    )
    day_of_week = models.IntegerField(
        choices=DAY_CHOICES, 
        verbose_name="曜日"
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_CHOICES,
        default='dinner',
        verbose_name="食事の種類"
    )
    servings = models.PositiveIntegerField(
        default=2, 
        verbose_name="人数分",
        help_text="この日に作る人数分"
    )
    notes = models.TextField(
        blank=True, 
        verbose_name="メモ",
        help_text="調理時の注意点など"
    )

    class Meta:
        verbose_name = "週献立レシピ"
        verbose_name_plural = "週献立レシピ"
        ordering = ['day_of_week', 'meal_type']
        unique_together = ['weekly_menu', 'day_of_week', 'meal_type']

    def __str__(self):
        day_name = dict(self.DAY_CHOICES)[self.day_of_week]
        meal_name = dict(self.MEAL_CHOICES)[self.meal_type]
        return f"{self.weekly_menu.name} - {day_name}{meal_name}: {self.recipe.name}"

    @property
    def date(self):
        """実際の日付を取得"""
        return self.weekly_menu.start_date + timedelta(days=self.day_of_week)


class MonthlyMenu(models.Model):
    """月単位の献立（週献立の組み合わせ）"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="ユーザー"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="月献立名",
        help_text="例: 2024年1月の献立"
    )
    year = models.PositiveIntegerField(verbose_name="年")
    month = models.PositiveIntegerField(verbose_name="月")
    description = models.TextField(
        blank=True, 
        verbose_name="説明・メモ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "月献立"
        verbose_name_plural = "月献立"
        ordering = ['-year', '-month']
        unique_together = ['user', 'year', 'month']

    def __str__(self):
        return f"{self.name} ({self.year}年{self.month}月)"


class MonthlyMenuWeek(models.Model):
    """月献立の週献立割り当て"""
    monthly_menu = models.ForeignKey(
        MonthlyMenu, 
        on_delete=models.CASCADE, 
        related_name='weekly_menus',
        verbose_name="月献立"
    )
    weekly_menu = models.ForeignKey(
        WeeklyMenu, 
        on_delete=models.CASCADE, 
        verbose_name="週献立"
    )
    week_number = models.PositiveIntegerField(
        verbose_name="週番号",
        help_text="その月の第何週か（1-5）"
    )

    class Meta:
        verbose_name = "月献立週"
        verbose_name_plural = "月献立週"
        ordering = ['week_number']
        unique_together = ['monthly_menu', 'week_number']

    def __str__(self):
        return f"{self.monthly_menu.name} 第{self.week_number}週: {self.weekly_menu.name}" 